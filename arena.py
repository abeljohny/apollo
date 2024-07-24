import ollama

from config import Config
from orchestrator import Orchestrator


class Arena(object):
    def __init__(self, discussion_topic: str, file, config: Config) -> None:
        """Initializes an environment (Arena) for LLMs to discourse"""
        # self._discussion_topic = discussion_topic
        self._config = config
        self._orchestrator = Orchestrator(discussion_topic, file, config)

    # def converse(self):
    #     consensus_reached = False
    #     model_idx = 0
    #     turn_count = -1
    #     msgs = [
    #         {"role": "system", "content": f"{self._config.system_prompt}"},
    #         {"role": "user", "content": f"{self._discussion_topic}"},
    #     ]
    #
    #     while not consensus_reached:
    #         selected_model_idx = model_idx % len(self._config.selected_agents)
    #         if selected_model_idx == 0:
    #             turn_count += 1
    #
    #         model = self._config.selected_agents[selected_model_idx]
    #         stream = ollama.chat(
    #             model=model.strip(),
    #             messages=msgs,
    #             stream=True,
    #         )
    #
    #         partial_response = ""
    #         if selected_model_idx == 0 and turn_count == 0:
    #             yield f"data:Turn {turn_count} for {model.title()[:-3]} :: \n\n"
    #         else:
    #             yield f"data:<br /><br />Turn {turn_count} for {model} :: \n\n"
    #         for chunk in stream:
    #             partial_response += chunk["message"]["content"]
    #             yield f'data: {chunk["message"]["content"]}\n\n'
    #
    #         msgs.append(
    #             {
    #                 "role": "user",
    #                 "content": f"{model}: {partial_response}",
    #             },
    #         )
    #
    #         consensus_reached = Util.consensus_reached(partial_response)
    #
    #         model_idx += 1
    #
    #         if turn_count > self._config.max_n_o_turns:
    #             yield "data:<br /><br />-- TERMINATING CONVERSATION: MAX TURNS REACHED --\n\n"
    #             return
    #
    #     yield "data:<br /><br />-- CONSENSUS REACHED BY ALL PARTIES --\n\n"

    @staticmethod
    def available_system_models():
        """Returns Ollama models already available in system"""
        system_models = ollama.list()
        return [model["name"] for model in system_models["models"]]

    def execute(self):
        yield from self._orchestrator.initiate_debate()
