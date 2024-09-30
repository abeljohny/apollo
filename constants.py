from enum import Enum


class FilePaths(Enum):
    """File Paths to configuration files"""

    SYSTEM_PROMPT = "config/sysprompt.txt"
    SYSTEM_PROMPT_COURT = "config/sysprompt_lawyer.txt"


class SupportedFileTypes(Enum):
    PDF = ".pdf"
    ZIP = ".zip"


class EscapeSequences(Enum):
    NEWLINE = "\n"


class ConversationalMarkers(Enum):
    RAG_QUERY = "{query:"


class ModelNames(Enum):
    LLAMA_INSTRUCT = "llama3.1:8b-instruct-q8_0"
    LLAMA = "llama3.1:latest"
    MISTRAL_INSTRUCT = "mistral:7b-instruct"
    MISTRAL = "mistral:7b"
    GEMMA_INSTRUCT = "gemma2:9b-instruct-q8_0"
    GEMMA = "gemma2:latest"
    QWEN = "qwen2:latest"


class Defaults(Enum):
    AGENTS: list[str] = [
        ModelNames.GEMMA_INSTRUCT.value,
        ModelNames.LLAMA_INSTRUCT.value,
    ]
    MAX_N_O_TURNS = 6
    DATABASE = {"host": "localhost", "port": 6379}


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
    LAWYER_TOGGLE = "lawyerToggle"
    CONSENSUS_TOGGLE = "consensusToggle"


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
    RAG = "<span class='font-bold text-indigo-600'>RAG System: {data}</span>"


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
    classic_rr = "Classic Round-Robin Discussion"
    summarized = "Summarized Discussion"


class Settings(Enum):
    FINAL_DECISION = "on"
    ALL_CONVO = "off"  # Summarized View
    SHOW_HARMFULNESS = "on"
    HIDE_HARMFULNESS = "off"
    LAWYER_ON = "on"
    LAWYER_OFF = "off"
    MODERATE_CONSENSUS = "on"
    HIGH_CONSENSUS = "off"


class Consensus(Enum):
    HIGH_CONSENSUS = 1
    MODERATE_CONSENSUS = 0.5
    NO_CONSENSUS = 0
