from agent import Agent
from config import Config
from constants import ConversationalMarkers
from utils.file_manager import FileManager


class Orchestrator:
    """Responsible for coordinating LLMs"""

    def __init__(self, topic: str, file, config: Config):
        self._topic: str = topic
        self._file: str = FileManager.parse_file(file)
        self._config: Config = config
        self._agents: list[Agent] = [
            Agent(llm, idx, self._config)
            for idx, llm in enumerate(self._config.selected_agents)
        ]
        self._consensus = {
            "final_consensus_reached": False,
            "intermediate_consensus_reached": False,
            "agents_in_consensus": set(),
        }
        self._turn: int = -1

    @property
    def _context(self):
        return {
            "n_o_agents": len(self._agents),
            "agent_names": [agent.name for agent in self._agents],
            "current_agent": None,
            "turn": self._turn,
            "consensus": self._consensus,
        }

    @staticmethod
    def consensus_detected(conversation_piece: str) -> bool:
        """Checks if consensus is reached on a bit of conversation"""
        return (
            ConversationalMarkers.CONSENSUS_REACHED.value in conversation_piece.lower()
        )

    def initiate_debate(self):
        agent_idx: int = 0
        msgs = [
            {"role": "system", "content": f"{self._config.system_prompt}"},
        ]

        if self._file is not None:
            msgs.append(
                {
                    "role": "user",
                    "content": f"Topic: {self._topic}",
                }
            )
            msgs.append(
                {
                    "role": "user",
                    "content": f"Attached File: {self._file.strip()[:1000]}",
                }
            )
        else:
            msgs.append({"role": "user", "content": f"Topic: {self._topic}"})

        while not self._consensus["final_consensus_reached"]:
            context = self._context

            # select agent
            selected_agent_idx = agent_idx % len(self._agents)
            if selected_agent_idx == 0:
                self._turn += 1
            agent = self._agents[selected_agent_idx]
            agent_idx += 1

            yield from agent.chat(context, msgs)
            yield f"data: <br /><br />\n\n"
            msgs = msgs[:-1]
            msgs.append(
                {"role": "user", "content": f"{agent.name}: {agent.last_response}"}
            )

            if self.consensus_detected(agent.last_response):
                self._consensus["intermediate_consensus_reached"] = True
                self._consensus["agents_in_consensus"].add(agent.name)

            if (
                len(context["consensus"]["agents_in_consensus"])
                == context["n_o_agents"]
            ):
                self._consensus["final_consensus_reached"] = True
                yield "data:<br /><br />-- SYSTEM: CONSENSUS REACHED BY ALL PARTIES --\n\n"
                return

            if self._turn == self._config.max_n_o_turns:
                yield "data:<br /><br />-- SYSTEM: TERMINATING DISCUSSION AS MAX TURNS REACHED --\n\n"
                return

        # model_idx = 0
        # turn_count = -1
        # msgs = [
        #     {"role": "system", "content": f"{self._config.system_prompt}"},
        #     {"role": "user", "content": f"{self._topic}"},
        # ]
        #
        # while not self._consensus:
        #     selected_model_idx = model_idx % len(self._agents)
        #     if selected_model_idx == 0:
        #         turn_count += 1
        #
        #     model = self._config.selected_agents[selected_model_idx]
        #     stream = ollama.chat(
        #         model=model.strip(),
        #         messages=msgs,
        #         stream=True,
        #     )
        #
        #     partial_response = ""
        #     if selected_model_idx == 0 and turn_count == 0:
        #         yield f"data:Turn {turn_count} for {model.title()[:-3]} :: \n\n"
        #     else:
        #         yield f"data:<br /><br />Turn {turn_count} for {model} :: \n\n"
        #     for chunk in stream:
        #         partial_response += chunk["message"]["content"]
        #         yield f'data: {chunk["message"]["content"]}\n\n'
        #
        #     msgs.append(
        #         {
        #             "role": "user",
        #             "content": f"{model}: {partial_response}",
        #         },
        #     )
        #
        #     consensus_reached = Util.consensus_reached(partial_response)
        #
        #     model_idx += 1
        #
        #     if turn_count > self._config.max_n_o_turns:
        #         yield "data:<br /><br />-- TERMINATING CONVERSATION: MAX TURNS REACHED --\n\n"
        #         return
        #
        # yield "data:<br /><br />-- CONSENSUS REACHED BY ALL PARTIES --\n\n"
