# price_scraper.py
import os
import datetime
import time

import wget
from dotenv import load_dotenv

load_dotenv()


def download(day=None, month=None, year=None):
    today = datetime.date.today()
    if day is None:
        day = today.day
    if month is None:
        month = today.month
    if year is None:
        year = today.year

    try:
        date_obj = datetime.date(year, month, day)
    except ValueError:
        print("Invalid date")
        return None

    if date_obj.weekday() >= 5:
        print(f"Date: {date_obj} is a weekend")
        return None

    date_str_for_db = date_obj.strftime('%d-%m-%Y')
    date_str_for_url = f"{day}-{month}-{year}"

    URL = os.getenv("URL")
    URL3 = os.getenv("URL3")
    filename = os.getenv("FILENAME")

    full_url = URL + date_str_for_url + URL3

    try:
        if os.path.exists(filename):
            safe_remove(filename)

        wget.download(full_url, filename)
        print(f"\nDownload successfully completed for date: {date_str_for_db}")
        return date_str_for_db
    except Exception as e:
        print("Error: ", e)
        return None


def safe_remove(filename, retries=5, delay=1):
    for i in range(retries):
        try:
            if os.path.exists(filename):
                os.remove(filename)
            return True
        except PermissionError:
            print(f"Plik {filename} jest używany, próba {i+1}/{retries}...")
            time.sleep(delay)
    return False