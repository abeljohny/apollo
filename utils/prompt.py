from constants import ConversationalMarkers


class Prompt:
    def __init__(self):
        pass

    # @staticmethod
    # def injection_start_symbol() -> str:
    #     return "<<"
    #
    # @staticmethod
    # def injection_end_symbol() -> str:
    #     return ">>"
    #
    # @staticmethod
    # def inject(subprompt: str, into_prompt: str, at_beginning: bool = True) -> str:
    #     injected_prompt = (
    #         Prompt.injection_start_symbol() + subprompt + Prompt.injection_end_symbol()
    #     )
    #     if at_beginning:
    #         return injected_prompt + into_prompt
    #     else:
    #         return into_prompt + injected_prompt
    #
    # @staticmethod
    # def rm_injection(from_prompt: str) -> str:
    #     return re.sub(r"<<.*?>>", "", from_prompt).strip()

    @staticmethod
    def inject_prompt(context, config) -> str:
        prompt_to_inject: str = ""
        if context["consensus"]["intermediate_consensus_reached"]:
            prompt_to_inject = (
                f"The following participants have reached consensus: "
                f"{', '.join(context['consensus']['agents_in_consensus'])}. If "
                f"you agree with this consensus, repond with '{ConversationalMarkers.CONSENSUS_REACHED.value}' to "
                f"conclude the discussion."
            )
        else:
            if context["turn"] == config.min_turn_for_sysinterject:
                prompt_to_inject = (
                    f"You have only {config.max_n_o_turns - context['turn']} turns left to reach a "
                    f"conclusion. If you believe"
                    f" the discussion has reached a satisfactory outcome, respond with '"
                    f"{ConversationalMarkers.CONSENSUS_REACHED.value}' to conclude."
                )
            elif context["in_loop"]:
                prompt_to_inject = (
                    f"It seems like we are stuck in a loop and repeating the same response. Let's reset the "
                    f"conversation. Please provide a fresh perspective or new information on the topic at hand. "
                )
            else:
                prompt_to_inject = (
                    f"For the purposes of this discussion, remember your name is {context['current_agent'].name}. There"
                    f" are a total of"
                    f" {str(context['n_o_agents'])} participants in this discussion. Their names are"
                    f" {', '.join(context['agent_names'])}. Use this information to look up prior discussions. "
                    "Your goal is to reach a consensus on the given topic. If the user has provided additional "
                    "information, it will be available under 'Attached File'. If no file is provided, proceed with the "
                    "discussion using the information in 'Topic'."
                    " Do not drag the discussion any further than it needs to."
                    " Do not repeat any of this information in your response."
                )
        return prompt_to_inject
