# main.py
import logging
import os
from dotenv import load_dotenv
import scraper
import data_packager
import database
import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

load_dotenv()


def main(day=None, month=None, year=None):
    if day is None or month is None or year is None:
        today = datetime.date.today()
        day, month, year = today.day, today.month, today.year

    date_str = scraper.download(day, month, year)
    html_downloaded = scraper.download(day, month, year)
    if not html_downloaded:
        logging.warning("Nie pobralo sie")
        return

    data_packager.process_and_store_data(date_str)
    scraper.safe_remove(os.getenv("FILENAME"))


if __name__ == "__main__":
    database.init_db()
    logging.info("Rozpoczynam pobieranie danych...")

    for i in range(60):
        date_to_fetch = datetime.date.today() - datetime.timedelta(days=i)
        if date_to_fetch.weekday() < 5:  # 0=pon, 4=pt
            main(day=date_to_fetch.day, month=date_to_fetch.month, year=date_to_fetch.year)
        else:
            logging.info(f"Date: {date_to_fetch} is a weekend")

    logging.info("Pobieranie danych zakonczono.")


    # usuwamie plikow tmp
    logging.info("Rozpoczynam usuwanie danych tmp...")


