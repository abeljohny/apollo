import ollama

from config import Config
from util_llm import UtilLLM


class Arena(object):
    def __init__(self, discussion_topic: str, participating_models: str) -> None:
        """Initializes an environment (Arena) for LLM models to discourse"""
        self._discussion_topic = discussion_topic
        self._participating_models = participating_models.strip().split(",")
        self._config = Config()

    def converse(self):
        consensus_reached = False
        model_idx = 0
        turn_count = -1
        msgs = [
            {"role": "system", "content": f"{self._config.system_prompt}"},
            {"role": "user", "content": f"{self._discussion_topic}"},
        ]

        while not consensus_reached:
            selected_model_idx = model_idx % len(self._participating_models)
            if selected_model_idx == 0:
                turn_count += 1

            model = self._participating_models[selected_model_idx]
            stream = ollama.chat(
                model=model.strip(),
                messages=msgs,
                stream=True,
            )

            partial_response = ""
            yield f"data:Turn {turn_count} for {model}\n\n"
            for chunk in stream:
                partial_response += chunk["message"]["content"]
                yield f'data: {chunk["message"]["content"]}\n\n'

            msgs.append(
                {
                    "role": "user",
                    "content": f"Turn {turn_count} for {model}: {partial_response}",
                },
            )

            consensus_reached = UtilLLM.consensus_reached(partial_response)

            model_idx += 1
