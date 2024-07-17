from abc import ABC, abstractmethod


class ModelABC(ABC):
    def __init__(self):
        pass

    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    @property
    @abstractmethod
    def last_response(self) -> str:
        pass

    @abstractmethod
    def chat(self, context) -> str:
        pass
