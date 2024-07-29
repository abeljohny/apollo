from constants import AgentBehaviors, ConversationalMarkers


class Prompt:
    def __init__(self):
        pass

    @staticmethod
    def truncate_prompt(prompt: str, maxlen: int = 1000):
        if len(prompt) > maxlen:
            return prompt[:maxlen] + "..."
        return prompt

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
        elif context["consensus"]["final_consensus_reached"]:
            prompt_to_inject = (
                f"Please summarize all discussions that have taken place after consensus was reached. "
                f"Include key points, main topics discussed, and any new insights or conclusions "
                f"drawn since reaching the consensus. Your summary should be clear and concise."
            )
        else:
            if context["in_loop"]:
                prompt_to_inject = (
                    f"It seems like we are stuck in a loop and repeating the same response. Let's reset the "
                    f"conversation. Please provide a fresh perspective or new information on the topic at hand. "
                )
            elif (
                config.agent_behavior == AgentBehaviors.summarized.value
                and context["turn_updated"] is True
            ):
                prompt_to_inject = (
                    f"Please summarize all discussions that have taken place up to this point. Include "
                    f"key points, and main topics. Your summary should be clear and concise."
                )
            elif context["turn"] == config.min_turn_for_sysinterject:
                prompt_to_inject = (
                    f"You have only {config.max_n_o_turns - context['turn']} turn(s) left to reach a "
                    f"conclusion. If you believe"
                    f" the discussion has reached a satisfactory outcome, respond with '"
                    f"{ConversationalMarkers.CONSENSUS_REACHED.value}' to conclude."
                )
            else:
                prompt_to_inject = (
                    f"For the purposes of this discussion, remember your name is {context['current_agent'].name}. There"
                    f" are a total of"
                    f" {str(context['n_o_agents'])} participants in this discussion. Their names are"
                    f" {', '.join(context['agent_names'])}. Use this information to look up prior discussions. "
                    "Your goal is to reach a consensus on the given topic. If the user has provided additional "
                    "information, it will be available under 'Attached File'. If no file is provided, proceed with the "
                    "discussion using the information in 'Topic'. Be sure to include clear and detailed explanations "
                    "for your reasoning. Do not drag the discussion any further than it needs to."
                    " Do not repeat any of this information in your response."
                )
        return prompt_to_inject
