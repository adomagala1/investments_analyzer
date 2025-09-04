# scraper_reports.py
import requests
import sqlite3
import logging
from bs4 import BeautifulSoup

DB_NAME = "raporty_finansowe.db"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def init_db():
    """Inicjalizacja bazy danych."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS raporty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            spolka TEXT NOT NULL,
            pole TEXT NOT NULL,
            wartosci TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    logging.info("Baza danych gotowa.")


def fetch_html(url: str) -> str:
    """Pobiera HTML z podanego URL."""
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.text


def parse_report(html: str) -> list:
    """
    Parsuje raport finansowy (RZiS) i zwraca listę rekordów:
    [
      {'pole': 'IncomeRevenues', 'wartosci': ['21 433', '19 152', ...]},
      ...
    ]
    """
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("tr", {"data-field": True})
    records = []

    for row in rows:
        field = row.get("data-field", "").strip()
        tds = row.find_all("td", class_="h") + row.find_all("td", class_="h newest")
        values = []
        for td in tds:
            val_tag = td.find("span", class_="pv")
            if val_tag:
                value = val_tag.get_text(strip=True).replace("\xa0", " ")
                values.append(value)
        if field and values:
            records.append({"pole": field, "wartosci": values})

    return records


def save_to_db(spolka: str, records: list):
    """Zapisuje raporty do SQLite."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    for record in records:
        c.execute(
            "INSERT INTO raporty (spolka, pole, wartosci) VALUES (?, ?, ?)",
            (spolka, record["pole"], ", ".join(record["wartosci"]))
        )
    conn.commit()
    conn.close()
    logging.info(f"Zapisano {len(records)} rekordów dla spółki {spolka}")


def scrape_company(symbol: str):
    """Scrapuje raport finansowy dla jednej spółki."""
    url = f"https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/{symbol}"
    logging.info(f"Pobieranie raportu: {symbol}")
    html = fetch_html(url)
    records = parse_report(html)
    if records:
        save_to_db(symbol, records)
    else:
        logging.warning(f"Brak danych dla spółki {symbol}")


if __name__ == "__main__":
    init_db()
    # TEST: pobranie raportu dla 06N
    scrape_company("06N")
