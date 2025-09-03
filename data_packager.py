#data_packager.py
import re
import os
import json
import config
import database


def extract_rows_from_html(html):
    row_pattern = r"<tr[^>]*>(.*?)</tr>"
    rows = re.findall(row_pattern, html, re.DOTALL)

    data = {}
    cell_pattern = r'<td[^>]*>(?:<span[^>]*></span>)?([^<]+)</td>'

    for row in rows:
        cells = re.findall(cell_pattern, row, re.DOTALL)
        cells = [c.replace("\xa0", " ").replace("&nbsp;", " ").strip() for c in cells]
        if len(cells) == 8:
            ticker = cells[0]
            data[ticker] = {
                "currency": cells[1],
                "open": cells[2],
                "high": cells[3],
                "low": cells[4],
                "close": cells[5],
                "change_percent": cells[6],
                "volume": cells[7]
            }
    return data


def process_and_store_data(date_str: str):
    """Główna funkcja, która parsuje HTML i zapisuje dane do JSON i BAZY DANYCH."""
    try:
        filename = os.getenv("FILENAME")
        with open(filename, encoding="utf-8") as f:
            html_content = f.read()

        daily_data = extract_rows_from_html(html_content)
        if not daily_data:
            print("Nie udało się wyodrębnić danych z pliku HTML.")
            return

        out_name = f"{date_str}.json"
        full_path = os.path.join(config.data_path, out_name)
        with open(full_path, "w", encoding="utf-8") as file:
            json.dump(daily_data, file, ensure_ascii=False, indent=4)
        print(f"Dane zarchiwizowane w {out_name}")

        database.insert_daily_data(date_str, daily_data)

    except OSError as e:
        print(f"Błąd pliku: {e}")
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")
