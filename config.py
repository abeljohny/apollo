from constants import Defaults, FilePaths
from file_manager import FileManager


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
        self._agent_behavior = "None"

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
