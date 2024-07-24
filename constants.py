from enum import Enum


class FilePaths(Enum):
    """File Paths to configuration files"""

    SYSTEM_PROMPT = "config/sysprompt.txt"


class SupportedFileTypes(Enum):
    PDF = ".pdf"


class ConversationalMarkers(Enum):
    CONSENSUS_REACHED = "{consensus-reached}"


class ModelNames(Enum):
    """Supported LLMs"""

    LLAMA = "llama3:latest"
    GEMMA = "gemma2:latest"
    MISTRAL = "mistral:instruct"
    QWEN = "qwen2:latest"


class Defaults(Enum):
    # AGENTS: list[str] = ["llama3:latest", "mistral:7b"]
    AGENTS: list[str] = [ModelNames.GEMMA.value, ModelNames.GEMMA.value]


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
    VIEW_TOGGLE = "viewToggle"


class SystemParams(Enum):
    MIN_TURN_FOR_SYSINTERJECT = 10
    DEFAULT_MIN_TURN_FOR_SYSINTERJECT = -100
    MIN_LOOP_FOR_SYSINTERJECT = 3
    MAX_LOOKBACK_FOR_LOOP_DETECTION = 5


class Formatting(Enum):
    LINE_BREAK = "<br />"
    SYSPROMPT = "<div style='color: green; font-weight: bold;'><br />-- SYSTEM: {prompt} --</div>"


class SystemPrompts(Enum):
    CONSENSUS_REACHED = Formatting.SYSPROMPT.value.format(
        prompt="consensus reached by all parties."
    )
    MAX_TURNS_REACHED = Formatting.SYSPROMPT.value.format(
        prompt="terminating discussion as max turns reached."
    )
    LOOP_DETECTED = Formatting.SYSPROMPT.value.format(
        prompt="loop detected: attempting to realign agents and restore proper flow."
    )


class AgentBehaviors(Enum):
    classic_rr = "Classic Round-Robin Debate"
    summarized = "Summarized Discussion"
    devils_advocate = "Devil's Advocate Debate"


class Settings(Enum):
    FINAL_DECISION = "on"
    ALL_CONVO = "off"
