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

    LLAMA = "llama3.1:latest"
    GEMMA = "gemma2:latest"
    MISTRAL = "mistral:7b"
    QWEN = "qwen2:latest"


class Defaults(Enum):
    AGENTS: list[str] = [ModelNames.LLAMA.value, ModelNames.MISTRAL.value]
    MAX_N_O_TURNS = 6
    DATABASE_HOST = "localhost"
    DATABASE_PORT = 6379


class Templates(Enum):
    """HTML Templates used in Application"""

    INDEX = "index.html"
    CHAT = "chat.html"
    PRIOR = "prior.html"
    PRIOR_INSTANCE = "prior_instance.html"
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
    BIAS_TOGGLE = "biasToggle"


class SystemParams(Enum):
    MIN_PCT_BEFORE_SYSINTERJECT = 70
    MIN_LOOP_FOR_SYSINTERJECT = 3
    MAX_LOOKBACK_FOR_LOOP_DETECTION = 5
    BIAS_THRESHOLD_PCT = 50


class Formatting(Enum):
    LINE_BREAK = "<br />"
    SYSPROMPT = "<div style='color: green; font-weight: bold;'><br />-- SYSTEM: {prompt} --</div>"
    HARMFUL_RESPONSE = (
        "<span class='font-bold text-red-500'>Harmful Response: {data}</span>"
    )
    HARMLESS_RESPONSE = (
        "<span class='font-bold text-green-500'>Harmless Response</span>"
    )
    CONVERSATION = "-- {prompt} --<br /><br />{conversation}"


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
    devils_advocate = "Penalized Turn-Limit Debates"


class Settings(Enum):
    FINAL_DECISION = "on"
    ALL_CONVO = "off"  # Summarized View
    SHOW_HARMFULNESS = "on"
    HIDE_HARMFULNESS = "off"
