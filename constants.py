from enum import Enum


class FilePaths(Enum):
    """File Paths to configuration files"""

    SYSTEM_PROMPT = "config/sysprompt.txt"


class SupportedFileTypes(Enum):
    PDF = ".pdf"


class ConversationalMarkers(Enum):
    CONSENSUS_REACHED = "{consensus-reached}"


class Defaults(Enum):
    AGENTS: list[str] = ["llama3:latest", "mistral:7b"]


class Templates(Enum):
    """HTML Templates used in Application"""

    INDEX = "index.html"
    CHAT = "chat.html"
    SETTINGS = "settings.html"


class ElementNames(Enum):
    """Element Names for HTML tags"""

    DISCUSSION_TOPIC = "comment"
    FILE_CONTENTS = "fileContents"
    FILE_NAME = "fileNameInput"
    SYSPROMPT = "about"
    MAX_N_O_TURNS = "turnsCounter"
    SELECTED_AGENTS = "selectedModels[]"
    AGENT_BEHAVIOR = "agentBehavior"


class ModelNames(Enum):
    """Supported LLMs"""

    LLAMA = "llama3:latest"
    GEMMA = "gemma2:latest"
    MISTRAL = "mistral:instruct"
    QWEN = "qwen2:latest"


class ConfigParams(Enum):
    MIN_TURN_FOR_SYSINTERJECT = 10
    DEFAULT_MIN_TURN_FOR_SYSINTERJECT = -100
