from constants import Defaults, FilePaths


class Config(object):
    _quiet: bool = True
    _agents: list[str] = []
    _sysprompt: str = None
    _custom_sysprompt: bool = False
    _DEFAULT_SYSPROMPT: str = None

    def __init__(self):
        """Loads configuration files so that they can be made accessible as properties"""
        with open(FilePaths.SYSTEM_PROMPT.value, "r") as file:
            self._sysprompt = _DEFAULT_SYSPROMPT = file.read()

        self._agents = Defaults.AGENTS.value
        self._max_n_o_turns = 10

    @property
    def system_prompt(self, get_custom_prompt: bool = True) -> str:
        if get_custom_prompt:
            if self._custom_sysprompt:
                return self._sysprompt
            else:
                return ""
        else:
            return self._sysprompt

    @property
    def max_n_o_turns(self):
        return self._max_n_o_turns

    @property
    def selected_agents(self) -> list[str]:
        return self._agents

    def set_system_prompt(self, sysprompt: str) -> None:
        if sysprompt.isspace():
            self._sysprompt = self._DEFAULT_SYSPROMPT
        self._sysprompt = sysprompt
        self._custom_sysprompt = True

    def set_max_turns(self, turns: int):
        self._max_n_o_turns = turns

    def set_agents(self, agents: list[str]):
        self._agents = agents
