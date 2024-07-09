from enum import Enum


class DatabaseKeys(Enum):
    """Redis Database Keys"""

    TOPIC = "topic"
    MODELS = "models"


class FilePaths(Enum):
    """File Paths to configuration files"""

    SYSTEM_PROMPT = "config/sysprompt.txt"


class ConversationalMarkers(Enum):
    CONSENSUS_REACHED = "consensus reached"
