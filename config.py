from constants import Defaults, FilePaths, SystemParams
from utils.file_manager import FileManager


class Config(object):
    _quiet: bool = True
    _agents: list[str] = []
    _sysprompt: str = None
    _custom_sysprompt: bool = False
    _DEFAULT_SYSPROMPT: str = None

    def __init__(self):
        """Loads configuration files so that they can be made accessible as properties"""
        self._sysprompt = _DEFAULT_SYSPROMPT = FileManager.read_file(
            FilePaths.SYSTEM_PROMPT.value
        )
        self._max_n_o_turns = 10
        self._agents = Defaults.AGENTS.value
        self._agent_behavior = None
        self._discussion_topic = ""
        self._filecontent = None
        self._filename = None
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
    def discussion_topic(self) -> str:
        return self._discussion_topic

    @property
    def filecontent(self) -> str:
        return self._filecontent

    @property
    def filename(self) -> str:
        return self._filename

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

    def set_agents(self, agents: list[str]):
        self._agents = agents

    def set_agent_behavior(self, behavior: str):
        self._agent_behavior = behavior

    def set_discussion_topic(self, topic: str):
        self._discussion_topic = topic

    def set_filecontent(self, filecontent: str):
        self._filecontent = filecontent

    def set_filename(self, filename: str):
        self._filename = filename

    def _calc_min_turn_for_sysinterject(self) -> int:
        if self.max_n_o_turns >= SystemParams.MIN_TURN_FOR_SYSINTERJECT.value:
            return self.max_n_o_turns - 2
        return SystemParams.DEFAULT_MIN_TURN_FOR_SYSINTERJECT.value
