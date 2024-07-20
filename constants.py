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


class SystemParams(Enum):
    MIN_TURN_FOR_SYSINTERJECT = 10
    DEFAULT_MIN_TURN_FOR_SYSINTERJECT = -100
    MIN_LOOP_FOR_SYSINTERJECT = 3
    MAX_LOOKBACK_FOR_LOOP_DETECTION = 5


class SystemPrompts(Enum):
    CONSENSUS_REACHED = "<br /><br />-- SYSTEM: consensus reached by all parties. --"
    MAX_TURNS_REACHED = (
        "<br /><br />-- SYSTEM: terminating discussion as max turns reached. --"
    )
    LOOP_DETECTED = "<br /><br />-- SYSTEM: Loop detected. Attempting to realign agents and restore proper flow."


class Formatting(Enum):
    LINE_BREAK = "<br />"
