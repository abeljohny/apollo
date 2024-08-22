import ollama

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

    @staticmethod
    def available_system_models():
        """Returns Ollama models already available in system"""
        system_models = ollama.list()
        return [model["name"] for model in system_models["models"]]
