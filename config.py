#config.py
import os

data_path = "./data"
shits_path = "./shits"


def create_paths():
    paths = [
        {"data_path": data_path}
    ]

    for path_dict in paths:
        path = path_dict["data_path"]
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Folder utworzony: {path}")
        else:
            print(f"Folder już istnieje: {path}")


create_paths()
