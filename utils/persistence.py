from utils.database import Database
from utils.file_manager import FileManager


class Persistence:
    """Manages Disk and Database read-writes"""

    def __init__(self):
        self._db = Database()
        self._file_manager = FileManager()

    @property
    def file_manager(self):
        return self._file_manager

    @property
    def database(self):
        return self._db
