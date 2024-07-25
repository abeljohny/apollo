import ollama

from constants import ModelNames
from models.modelABC import ModelABC


class Mistral(ModelABC):
    def __init__(self):
        super().__init__()
        self._response = ""

    @staticmethod
    def name() -> str:
        return ModelNames.MISTRAL.value

    @property
    def last_response(self) -> str:
        return self._response

    def chat(self, context) -> str:
        stream = ollama.chat(
            model=Mistral.name(),
            messages=context,
            stream=True,
        )
        self._response = ""
        for chunk in stream:
            yield f'data: {chunk["message"]["content"]}\n\n'
            self._response += chunk["message"]["content"]
