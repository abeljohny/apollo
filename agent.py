from constants import ConversationalMarkers, ModelNames
from models.gemma import Gemma
from models.modelABC import ModelABC


class Agent:
    """Encapsulates an LLM into an Agent i.e. assigning it memory"""

    def __init__(self, llm_name: str, seed: int):
        self._model = self._instantiate_model(llm_name)
        self._model_seed = seed

    @property
    def name(self) -> str:
        """model names are in format <model name>:<parameter count | latest>. _model_seed ensures identical models
        have unique names."""
        return self._model.name().split(":")[0].title() + str(self._model_seed)

    @staticmethod
    def _instantiate_model(llm_name: str) -> ModelABC:
        match llm_name:
            case ModelNames.GEMMA.value:
                return Gemma()

    @property
    def last_response(self) -> str:
        return self._model.last_response

    def chat(self, context, msgs) -> str:
        if context["intermediate_consensus_reached"]:
            subprompt: str = (
                f"The following participants have reached consensus: {', '.join(context['agents_in_consensus'])}. If "
                f"you agree with this consensus, repond with '{ConversationalMarkers.CONSENSUS_REACHED.value}' to "
                f"conclude the discussion."
            )
        else:
            subprompt: str = (
                f"For the purposes of this discussion, remember your name is {self.name}. There are a total of"
                f" {str(context['n_o_agents'])} participants in this discussion. Their names are"
                f" {', '.join(context['agent_names'])}. Use this information to look up prior discussions. "
                "Remember your goal is to reach consensus on a topic. "
                "Do not drag the discussion any further than it needs to. Do not repeat any of this information in your"
                " response."
            )

        msgs.append({"role": "user", "content": f"{subprompt}"})
        yield f"data: {self.name}: \n\n"
        yield from self._model.chat(msgs)
