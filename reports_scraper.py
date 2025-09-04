# reports_scraper.py
import requests
import sqlite3
import logging
from bs4 import BeautifulSoup
from database import save_to_raporty_db, init_reports_db, get_all_tickers


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


def scrape_company(symbol: str):
    """Scrapuje raport finansowy dla jednej spółki."""
    url = f"https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/{symbol}"
    logging.info(f"Pobieranie raportu: {symbol}")
    html = fetch_html(url)
    records = parse_report(html)
    if records:
        save_to_raporty_db(symbol, records)
    else:
        logging.warning(f"Brak danych dla spółki {symbol}")


def scrape_all_companies():
    tickers = get_all_tickers()
    logging.info(f"Scrapuje {len(tickers)} spółek...")
    try:
        for ticker in tickers:
            scrape_company(ticker)
    except Exception as e:
        logging.error(f"Error during scraping: {e}")


if __name__ == "__main__":
    # init_raporty_db()
    tickers = get_all_tickers()
    for ticker in tickers:
        scrape_company(ticker)
