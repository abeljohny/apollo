from constants import FilePaths


class Config(object):
    quiet: bool = True

    def __init__(self):
        """Loads configuration files so that they can be made accessible as properties"""
        with open(FilePaths.SYSTEM_PROMPT.value, "r") as file:
            self._sysprompt = file.read()

    @property
    def system_prompt(self) -> str:
        return self._sysprompt
