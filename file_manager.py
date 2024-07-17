import os
from typing import AnyStr


class FileManager(object):
    def __init__(self):
        pass

    @staticmethod
    def file_exists(filepath: str) -> bool:
        """Checks if filepath exists.
        :param filepath: file path
        """
        return os.path.exists(filepath)

    @staticmethod
    def read_file(filepath: str) -> AnyStr:
        if FileManager.file_exists(filepath):
            with open(filepath, "r") as file:
                return file.read()
