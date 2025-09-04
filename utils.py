import logging
import os
import sqlite3

raporty_db = "raporty_finansowe.db"


current_dir = os.path.dirname(os.path.abspath(__file__))


def delete_data_files():
    files_deleted = []
    for filename in os.listdir(current_dir):
        if filename.endswith(".tmp"):
            files_deleted.append(filename)
            os.remove(os.path.join(current_dir, filename))

    logging.info(f"Usunieto plikow {len(files_deleted)} i takie np: {files_deleted}")


def get_raport_db_connection():
    conn = sqlite3.connect(raporty_db)
    conn.row_factory = sqlite3.Row
    return conn
