import ollama

from constants import ConversationalMarkers


class Util(object):
    @staticmethod
    def available_system_models():
        """Returns Ollama models already available in system"""
        system_models = ollama.list()
        return [model["name"] for model in system_models["models"]]

    @staticmethod
    def consensus_reached(convo_bit: str) -> bool:
        """Checks if consensus is reached on a bit of conversation"""
        return ConversationalMarkers.CONSENSUS_REACHED.value in convo_bit.lower()

    # @staticmethod
    # def chat(on_topic, using_models):
    #     stream = ollama.chat(
    #         model="gemma",
    #         messages=[{"role": "user", "content": f"{on_topic}"}],
    #         stream=True,
    #     )
    #
    #     for chunk in stream:
    #         yield f'data:{chunk["message"]["content"]}\n\n'
    @staticmethod
    def agent_behaviors():
        return [
            "Classic Round-Robin Debate",
            "Summarized Discussion",
            "Devil's Advocate Debate",
        ]
