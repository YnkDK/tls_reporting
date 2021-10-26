from app.core import config
import os


def get_server_api():
    return config.SERVER_NAME


def get_test_data_path(filename: str = None) -> str:
    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    data_dir = os.path.join(dir_path, 'data')
    if filename:
        return os.path.join(data_dir, filename)
    return data_dir
