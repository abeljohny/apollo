from abc import ABC, abstractmethod


class ModelABC(ABC):
    def __init__(self, llm_name: str):
        self._name = llm_name

    @property
    def name(self) -> str:
        return self._name

    @property
    @abstractmethod
    def last_response(self) -> str:
        pass

    @abstractmethod
    def chat(self, context) -> str:
        pass
