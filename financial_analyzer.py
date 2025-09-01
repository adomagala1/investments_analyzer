# financial_analyzer.py
import re
import os
import json
import time
import wget
import config

# Lista pól z danymi finansowymi do wyciągnięcia
# Na podstawie prośby użytkownika i analizy kodu źródłowego biznesradar.pl
FINANCIAL_FIELDS = [
    "IncomeRevenues",           # Przychody netto ze sprzedaży
    "IncomeGrossProfit",        # Zysk (strata) brutto ze sprzedaży
    "IncomeEBIT",               # Zysk (strata) na działalności operacyjnej (EBIT)
    "IncomeBeforeTaxProfit",    # Zysk (strata) brutto
    "IncomeNetProfit",          # Zysk (strata) netto
]


def extract_financial_data_from_html(html_content):
    """
    Wyciąga dane finansowe dla określonych pól z treści HTML.
    Używa wyrażeń regularnych zgodnie z wymaganiami.
    """
    report_data = {}
    for field in FINANCIAL_FIELDS:
        # Wzorzec regex do znalezienia całego wiersza tabeli dla danego pola 'data-field'
        row_pattern = rf'<tr[^>]*data-field="{field}"[^>]*>(.*?)</tr>'
        row_match = re.search(row_pattern, html_content, re.DOTALL)

        if row_match:
            row_html = row_match.group(1)
            # Wzorzec regex do znalezienia pierwszej komórki z danymi liczbowymi
            # Komórki te mają klasę 'text-right'
            cell_pattern = r'<td class="text-right"[^>]*>([^<]+)</td>'
            cell_match = re.search(cell_pattern, row_html)

            if cell_match:
                # Czyszczenie wyodrębnionej wartości
                value = cell_match.group(1).strip()
                # Usunięcie spacji używanych jako separatory tysięcy
                value = value.replace(" ", "")
                report_data[field] = value
            else:
                report_data[field] = "N/A"
        else:
            report_data[field] = "N/A"

    return report_data


def enrich_with_financials(date_str: str):
    """
    Wczytuje plik JSON z danymi dziennymi, iteruje po tickerach,
    pobiera raporty finansowe i zapisuje wzbogacone dane z powrotem do tego samego pliku.
    """
    json_filename = f"{date_str}.json"
    full_path = os.path.join(config.data_path, json_filename)

    if not os.path.exists(full_path):
        print(f"Błąd: Plik {full_path} nie został znaleziony.")
        return

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            daily_data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Błąd podczas odczytu {full_path}: {e}")
        return

    print(f"\nWzbogacanie danych dla {date_str} o raporty finansowe...")

    temp_html_file = "temp_financial_report.html"

    for ticker in daily_data.keys():
        print(f"Pobieranie danych finansowych dla {ticker}...")

        # Uwaga: Ten format URL może nie działać dla niektórych tickerów (np. 'PEP' vs 'POLENERGIA').
        # Bardziej niezawodne rozwiązanie wymagałoby dodatkowego wyszukiwania,
        # ale na razie używamy bezpośrednio tickera.
        url = f"https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/{ticker}"

        try:
            if os.path.exists(temp_html_file):
                os.remove(temp_html_file)

            # Pobieranie strony w trybie cichym, aby nie zaśmiecać konsoli
            wget.download(url, out=temp_html_file, bar=None)

            with open(temp_html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            financial_data = extract_financial_data_from_html(html_content)
            daily_data[ticker]["financial_report"] = financial_data
            print(f"Pomyślnie dodano dane finansowe dla {ticker}.")

        except Exception as e:
            # Wyłapuje błędy HTTP z wget i inne problemy
            print(f"Nie można pobrać lub przetworzyć danych finansowych dla {ticker}. Błąd: {e}")
            daily_data[ticker]["financial_report"] = {"error": "data not found"}

        finally:
            if os.path.exists(temp_html_file):
                os.remove(temp_html_file)

        # Czekamy sekundę między zapytaniami, aby nie obciążać serwera
        time.sleep(1)

    # Zapisz zaktualizowane dane z powrotem do pliku JSON
    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(daily_data, f, ensure_ascii=False, indent=4)
        print(f"\nPomyślnie wzbogacono plik {json_filename} o dane finansowe.")
    except OSError as e:
        print(f"Błąd podczas zapisu zaktualizowanych danych do {full_path}: {e}")