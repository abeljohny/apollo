import ollama

from models.modelABC import ModelABC


class Default(ModelABC):
    def __init__(self, llm_name: str):
        super().__init__(llm_name)
        self._response = ""

    @property
    def name(self) -> str:
        return super().name

    @property
    def last_response(self) -> str:
        return self._response

    def chat(self, context) -> str:
        stream = ollama.chat(
            model=self.name,
            messages=context,
            stream=True,
        )
        self._response = ""
        for chunk in stream:
            yield f'data: {chunk["message"]["content"]}\n\n'
            self._response += chunk["message"]["content"]
