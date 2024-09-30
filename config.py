import random

from constants import Consensus, Defaults, FilePaths, Settings, SystemParams
from utils.file_manager import FileManager
from utils.persistence import Persistence


class Config(object):
    _agents: list[str] = []
    _sysprompt: str | None = None
    _all_sysprompts = {"default": None, "lawyer": None}
    _custom_sysprompt: bool = False
    _DEFAULT_SYSPROMPT: str = None

    def __init__(self):
        """Loads configuration files so that they can be made accessible as properties"""
        self._all_sysprompts["default"] = FileManager.read_file(
            FilePaths.SYSTEM_PROMPT.value
        )
        self._all_sysprompts["lawyer"] = FileManager.read_file(
            FilePaths.SYSTEM_PROMPT_COURT.value
        )
        self._sysprompt = _DEFAULT_SYSPROMPT = self._all_sysprompts["default"]
        self._max_n_o_turns = Defaults.MAX_N_O_TURNS.value

        # default agent selection
        available_models = Persistence.available_system_models()
        if set(Defaults.AGENTS.value).issubset(available_models):
            self._agents = Defaults.AGENTS.value
        elif available_models:
            self._agents.append(random.choice(available_models))
            self._agents.append(random.choice(available_models))

        self._agent_behavior = None
        self._view = Settings.ALL_CONVO.value
        self._bias = Settings.HIDE_HARMFULNESS.value
        self._lawyer = Settings.LAWYER_OFF.value
        self._consensus = Settings.HIGH_CONSENSUS.value
        self._discussion_topic = ""
        self._filecontent = None
        self._filename = None
        self._is_paused = False
        self._min_turn_for_sysinterject = self._calc_min_turn_for_sysinterject()

    @property
    def system_prompt(self) -> str:
        return self._sysprompt

    @property
    def max_n_o_turns(self):
        return self._max_n_o_turns

    @property
    def selected_agents(self) -> list[str]:
        return self._agents

    @property
    def agent_behavior(self) -> str:
        return self._agent_behavior

    @property
    def view(self) -> str:
        return self._view

    @property
    def bias(self) -> str:
        return self._bias

    @property
    def lawyer(self) -> str:
        return self._lawyer

    @property
    def consensus(self) -> str:
        return self._consensus

    @property
    def numerical_consensus(self) -> float:
        if self._consensus == Settings.MODERATE_CONSENSUS.value:
            return Consensus.MODERATE_CONSENSUS.value
        elif self._consensus == Settings.HIGH_CONSENSUS.value:
            return Consensus.HIGH_CONSENSUS.value
        else:
            return Consensus.NO_CONSENSUS.value

    @property
    def discussion_topic(self) -> str:
        return self._discussion_topic

    @property
    def filecontent(self) -> str:
        return self._filecontent

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def is_paused(self) -> bool:
        return self._is_paused

    @property
    def min_turn_for_sysinterject(self):
        return self._min_turn_for_sysinterject

    def set_system_prompt(self, sysprompt: str) -> None:
        if sysprompt.isspace():
            self._sysprompt = self._DEFAULT_SYSPROMPT
        self._sysprompt = sysprompt
        self._custom_sysprompt = True

    def set_max_turns(self, turns: int):
        self._max_n_o_turns = turns
        self._min_turn_for_sysinterject = self._calc_min_turn_for_sysinterject()

    def set_paused(self, paused: bool):
        self._is_paused = paused

    def set_agents(self, agents: list[str]):
        self._agents = agents

    def set_agent_behavior(self, behavior: str):
        self._agent_behavior = behavior

    def set_view(self, view: str):
        if view == "on":
            self._view = Settings.FINAL_DECISION.value
        else:
            self._view = Settings.ALL_CONVO.value

    def set_bias(self, bias: str):
        if bias == "on":
            self._bias = Settings.SHOW_HARMFULNESS.value
        else:
            self._bias = Settings.HIDE_HARMFULNESS.value

    def set_lawyer_mode(self, lawyer: str):
        if lawyer == "on":
            self._lawyer = Settings.LAWYER_ON.value
            self._sysprompt = self._all_sysprompts["lawyer"]
        else:
            self._lawyer = Settings.LAWYER_OFF.value
            self._sysprompt = self._all_sysprompts["default"]

    def set_consensus_mode(self, consensus: str):
        if consensus == "on":
            self._consensus = Settings.MODERATE_CONSENSUS.value
        else:
            self._consensus = Settings.HIGH_CONSENSUS.value

    def set_discussion_topic(self, topic: str):
        self._discussion_topic = topic

    def set_filecontent(self, filecontent: str):
        self._filecontent = filecontent

    def set_filename(self, filename: str):
        self._filename = filename

    def _calc_min_turn_for_sysinterject(self) -> int:
        return (
                SystemParams.MIN_PCT_BEFORE_SYSINTERJECT.value * self.max_n_o_turns // 100
        )
