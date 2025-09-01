# financial_analyzer.py
import re
import os
import json
import requests  # Używamy requests zamiast wget
from concurrent.futures import ThreadPoolExecutor, as_completed # Klucz do równoległości
import config

# Lista pól z danymi finansowymi do wyciągnięcia
FINANCIAL_FIELDS = [
    "IncomeRevenues",
    "IncomeGrossProfit",
    "IncomeEBIT",
    "IncomeBeforeTaxProfit",
    "IncomeNetProfit",
]

# Ustawiamy nagłówek User-Agent, aby udawać przeglądarkę. Zmniejsza to ryzyko blokady.
HTTP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Liczba jednoczesnych pobrań. Można dostosować w zależności od łącza internetowego.
MAX_WORKERS = 10


def extract_financial_data_from_html(html_content):
    """Wyciąga dane finansowe dla określonych pól z treści HTML."""
    report_data = {}
    for field in FINANCIAL_FIELDS:
        row_pattern = rf'<tr[^>]*data-field="{field}"[^>]*>(.*?)</tr>'
        row_match = re.search(row_pattern, html_content, re.DOTALL)
        if row_match:
            row_html = row_match.group(1)
            cell_pattern = r'<td class="text-right"[^>]*>([^<]+)</td>'
            cell_match = re.search(cell_pattern, row_html)
            if cell_match:
                value = cell_match.group(1).strip().replace(" ", "")
                report_data[field] = value
            else:
                report_data[field] = "N/A"
        else:
            report_data[field] = "N/A"
    return report_data

def fetch_financials_for_ticker(ticker: str):
    """
    Pobiera i przetwarza dane finansowe dla JEDNEJ spółki.
    Ta funkcja będzie wykonywana w osobnym wątku.
    """
    url = f"https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/{ticker}"
    try:
        # Używamy requests.get() - dane są pobierane do pamięci, bez zapisu na dysk
        response = requests.get(url, headers=HTTP_HEADERS, timeout=10)
        # Sprawdzamy, czy zapytanie się powiodło (kod 200)
        response.raise_for_status()

        financial_data = extract_financial_data_from_html(response.text)
        print(f"Pobrano dane dla: {ticker}")
        return ticker, financial_data
    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas pobierania danych dla {ticker}: {e}")
        return ticker, {"error": "data not found or connection error"}

def enrich_with_financials(date_str: str):
    """
    Wzbogaca plik JSON o dane finansowe, pobierając je równolegle dla wszystkich spółek.
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

    tickers = list(daily_data.keys())
    print(f"\nRozpoczynanie równoległego pobierania danych finansowych dla {len(tickers)} spółek...")

    # Używamy ThreadPoolExecutor do zarządzania pulą wątków
    # To jest serce optymalizacji!
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Tworzymy listę "zadań" do wykonania - jedno zadanie na każdy ticker
        future_to_ticker = {executor.submit(fetch_financials_for_ticker, ticker): ticker for ticker in tickers}

        # Zbieramy wyniki, gdy tylko się pojawią
        for future in as_completed(future_to_ticker):
            try:
                ticker, financial_data = future.result()
                if ticker in daily_data:
                    daily_data[ticker]["financial_report"] = financial_data
            except Exception as e:
                ticker_name = future_to_ticker[future]
                print(f"Wystąpił wyjątek podczas przetwarzania {ticker_name}: {e}")
                if ticker_name in daily_data:
                    daily_data[ticker_name]["financial_report"] = {"error": "processing failed"}

    # Zapisz zaktualizowane dane z powrotem do pliku JSON
    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(daily_data, f, ensure_ascii=False, indent=4)
        print(f"\nPomyślnie wzbogacono plik {json_filename} o dane finansowe.")
    except OSError as e:
        print(f"Błąd podczas zapisu zaktualizowanych danych do {full_path}: {e}")