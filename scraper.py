# scraper.py

import os
import datetime
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

    if date_obj.weekday() == 5 or date_obj.weekday() == 6:
        print(f"Date: {date_obj} is a weekend")
        return None

    URL = os.getenv("URL")
    URL3 = os.getenv("URL3")
    filename = os.getenv("FILENAME")

    date_str = f"{day}-{month}-{year}"
    full_url = URL + date_str + URL3

    try:
        wget.download(full_url, filename)
        print(f"\nDownload successfully completed for date: {date_str}, {full_url}")
        return date_str
    except Exception as e:
        print("Error: ", e)


def remove():
    filename = os.getenv("FILENAME")
    try:
        os.remove(filename)
        print(f"File {filename} has been deleted")
    except OSError as e:
        print("Error: ", e)
3