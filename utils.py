import os

current_dir = os.path.dirname(os.path.abspath(__file__))


def delete_data_files():
    for filename in os.listdir(current_dir):
        if filename.endswith(".tmp"):
            os.remove(os.path.join(current_dir, filename))
