# set the directory where data is stored
import os


def set_data_directory(path: str) -> str:
    """
    Set the directory location where the data is stored.
    """
    data_dir_name = path
    location = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), data_dir_name)
    return location
