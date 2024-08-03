from config import Config
from constants import AgentBehaviors
from models.default import Default
from models.modelABC import ModelABC
from utils.prompt import Prompt


class Agent:
    """Encapsulates an LLM into an Agent"""

    def __init__(self, llm_name: str, config: Config, seed: str = ""):
        self._model = self._instantiate_model(llm_name)
        self._model_seed = seed
        self._config = config

    @property
    def name(self) -> str:
        """Model names are in format <model name>:<parameter count | latest>. _model_seed ensures identical models
        have unique names."""
        return self._model.name.split(":")[0].title() + self._model_seed

    @property
    def underlying_model(self) -> ModelABC:
        return self._model

    @staticmethod
    def _instantiate_model(llm_name: str) -> ModelABC:
        match llm_name:
            case _:
                return Default(llm_name)

    @staticmethod
    def agent_behaviors(behavior=None):
        behaviors = {
            AgentBehaviors.classic_rr.value,
            AgentBehaviors.summarized.value,
        }
        if behavior is None:
            return list(behaviors)
        return [behavior] + list(behaviors - {behavior})

    @property
    def last_response(self) -> str:
        return self._model.last_response

    def chat(self, context, msgs) -> str:
        context["current_agent"] = self
        msgs.append(
            {
                "role": "user",
                "content": f"{Prompt.inject_prompt(context, self._config)}",
            }
        )
        yield f"data: {self.name}: \n\n"
        yield from self._model.chat(msgs)
