from config import Config
from orchestrator import Orchestrator
from utils.persistence import Persistence


class Arena(object):
    def __init__(
        self, discussion_topic: str, file, config: Config, persistence: Persistence
    ) -> None:
        """Initializes an environment (Arena) for LLMs to discourse"""
        self._config = config
        self._orchestrator = Orchestrator(discussion_topic, file, config, persistence)

    def execute(self):
        yield from self._orchestrator.initiate_discourse()
