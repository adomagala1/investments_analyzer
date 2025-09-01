# main.py
import scraper
import data_packager as analysis


def main(day=None, month=None, year=None):
    date_str = scraper.download(day, month, year)
    if not date_str:
        return
    analysis.anal_json(date_str)

    scraper.remove()


if __name__ == "__main__":
    for day in range(1, 5):
        # Aby przetestować, użyj dat z przeszłości, np. month=8, year=2023
        main(day=day, month=8, year=2025)
    # main()