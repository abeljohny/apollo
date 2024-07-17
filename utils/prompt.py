import re


class Prompt:
    def __init__(self):
        pass

    @staticmethod
    def injection_start_symbol() -> str:
        return "<<"

    @staticmethod
    def injection_end_symbol() -> str:
        return ">>"

    @staticmethod
    def inject(subprompt: str, into_prompt: str, at_beginning: bool = True) -> str:
        injected_prompt = (
            Prompt.injection_start_symbol() + subprompt + Prompt.injection_end_symbol()
        )
        if at_beginning:
            return injected_prompt + into_prompt
        else:
            return into_prompt + injected_prompt

    @staticmethod
    def rm_injection(from_prompt: str) -> str:
        return re.sub(r"<<.*?>>", "", from_prompt).strip()
