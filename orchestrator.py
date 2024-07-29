from collections import Counter

from agent import Agent
from config import Config
from constants import (
    AgentBehaviors,
    ConversationalMarkers,
    Formatting,
    Settings,
    SystemParams,
    SystemPrompts,
)
from utils.file_manager import FileManager
from utils.harmfulness_classifier import HarmfulnessClassifier
from utils.persistence import Persistence


class Orchestrator:
    """Responsible for coordinating LLMs"""

    def __init__(self, topic: str, file, config: Config, persistence: Persistence):
        self._topic: str = topic
        self._file: str = FileManager.parse_file(file)
        self._config: Config = config
        self._persistence: Persistence = persistence

        # instantiate Agents
        seen_models = {}
        self._agents = []
        for llm in self._config.selected_agents:
            if llm in seen_models:
                seen_models[llm] += 1
                self._agents.append(
                    Agent(llm_name=llm, seed=str(seen_models[llm]), config=self._config)
                )
            else:
                seen_models[llm] = 0
                self._agents.append(Agent(llm_name=llm, config=self._config))

        self._conversation_counter = Counter()
        self._in_loop: bool = False
        self._consensus = {
            "final_consensus_reached": False,
            "intermediate_consensus_reached": False,
            "agents_in_consensus": set(),
        }
        self._turn = {
            "turn": -1,
            "turn_updated": False,
        }

    @property
    def _context(self):
        return {
            "n_o_agents": len(self._agents),
            "agent_names": [agent.name for agent in self._agents],
            "current_agent": None,
            "turn": self._turn["turn"],
            "turn_updated": self._turn["turn_updated"],
            "consensus": self._consensus,
            "in_loop": self._in_loop,
        }

    @staticmethod
    def consensus_detected(conversation_piece: str) -> bool:
        """Checks if consensus is reached on a bit of conversation"""
        return (
            ConversationalMarkers.CONSENSUS_REACHED.value in conversation_piece.lower()
        )

    def _loop_detected(self, val: str) -> bool:
        self._conversation_counter[val] += 1

        if (
            self._conversation_counter.most_common(1)[0][1]
            > SystemParams.MIN_LOOP_FOR_SYSINTERJECT.value
        ):
            self._conversation_counter = Counter()
            return True

        if (
            len(self._conversation_counter)
            == SystemParams.MAX_LOOKBACK_FOR_LOOP_DETECTION.value
        ):
            self._conversation_counter = Counter()

        return False

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

        conversation_chunks = []
        while not self._consensus["final_consensus_reached"]:
            if self._config.is_paused:
                continue
            # select agent
            selected_agent_idx = agent_idx % len(self._agents)
            if selected_agent_idx == 0:
                self._turn["turn"] += 1
                if (
                    self._turn["turn"] > 0
                ):  # ignore for the very first turn as we don't have enough context
                    self._turn["turn_updated"] = True
            else:
                if (
                    self._turn["turn_updated"]
                    and self._config.agent_behavior == AgentBehaviors.summarized.value
                ):  # if prior turn was a new turn and Agents were asked to Summarize responses
                    agent_idx -= 1
                    selected_agent_idx = agent_idx % len(self._agents)
                self._turn["turn_updated"] = False

            agent = self._agents[selected_agent_idx]
            agent_idx += 1

            context = self._context

            if self._config.view == Settings.ALL_CONVO.value:
                yield from agent.chat(context, msgs)
                yield f"data: {Formatting.LINE_BREAK.value}\n\n"
                conversation_chunks.append(agent.name + ": " + agent.last_response)
                conversation_chunks.append(Formatting.LINE_BREAK.value)

                if self._config.bias == Settings.SHOW_HARMFULNESS.value:
                    harmfulness_metric = (
                        HarmfulnessClassifier.print_classify_harmfulness(
                            agent.last_response
                        )
                    )
                    yield f"data: {harmfulness_metric}\n\n"
                    conversation_chunks.append(harmfulness_metric)

                yield f"data: {Formatting.LINE_BREAK.value * 2}\n\n"
                conversation_chunks.append(Formatting.LINE_BREAK.value * 2)

            else:
                yield f"data: {agent.name} is responding...{Formatting.LINE_BREAK.value * 2}\n\n"
                conversation_chunks.append(
                    f"{agent.name} is responding...{Formatting.LINE_BREAK.value * 2}"
                )

                for _ in agent.chat(
                    context, msgs
                ):  # Agent's response is discarded for display if view is ON
                    pass

            msgs = msgs[:-1]  # remove agent-injected prompt

            response = f"{agent.name}: {agent.last_response}"
            msgs.append(
                {"role": "user", "content": f"{agent.name}: {agent.last_response}"}
            )

            if (
                self._config.agent_behavior == AgentBehaviors.summarized.value
                and self._turn["turn_updated"] is True
            ):
                msgs = [msgs[0], msgs[-1]]

            if self.consensus_detected(agent.last_response):
                self._consensus["intermediate_consensus_reached"] = True
                self._consensus["agents_in_consensus"].add(agent.name)

            if (
                len(context["consensus"]["agents_in_consensus"])
                == context["n_o_agents"]
            ):
                self._consensus["final_consensus_reached"] = True
                if (
                    self._config.agent_behavior == AgentBehaviors.summarized.value
                    and self._config.view == Settings.FINAL_DECISION.value
                ):
                    yield from agent.chat(self._context, msgs)
                yield f"data:{SystemPrompts.CONSENSUS_REACHED.value}\n\n"
                conversation_chunks.append(SystemPrompts.CONSENSUS_REACHED.value)
                conversation_chunks_str: str = "".join(conversation_chunks)
                self._persistence.database.write_conversation_to_db(
                    prompt=msgs[1]["content"], conversation=conversation_chunks_str
                )
                return

            if self._turn == self._config.max_n_o_turns:
                yield f"data:{SystemPrompts.MAX_TURNS_REACHED.value}\n\n"
                conversation_chunks.append(SystemPrompts.MAX_TURNS_REACHED.value)
                conversation_chunks_str: str = "".join(conversation_chunks)
                self._persistence.database.write_conversation_to_db(
                    prompt=msgs[1]["content"], conversation=conversation_chunks_str
                )
                return

            if self._loop_detected(response):
                self._in_loop = True
                yield f"data:{SystemPrompts.LOOP_DETECTED.value}\n\n"
                conversation_chunks.append(SystemPrompts.LOOP_DETECTED.value)
