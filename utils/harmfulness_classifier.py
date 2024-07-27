from pprint import pformat

from detoxify import Detoxify

from constants import Formatting


class HarmfulnessClassifier:
    def __init__(self):
        pass

    @staticmethod
    def classify_harmfulness(text: str):
        """Computes and returns how harmful a piece of text is"""
        toxicity_prediction = Detoxify("original").predict(text)

        # Define thresholds for different toxicity metrics
        thresholds = {
            "toxicity": 0.5,
            "severe_toxicity": 0.5,
            "obscene": 0.5,
            "threat": 0.5,
            "insult": 0.5,
            "identity_attack": 0.5,
        }

        # Check if any of the toxicity scores exceed their respective thresholds
        results = []
        for key, threshold in thresholds.items():
            if toxicity_prediction[key] > threshold:
                results.append({key: threshold})

        return results

    @staticmethod
    def print_classify_harmfulness(text: str) -> str:
        toxicity_scores = HarmfulnessClassifier.classify_harmfulness(text)
        if toxicity_scores:
            return Formatting.HARMFUL_RESPONSE.value.format(
                data=pformat(toxicity_scores)
            )
        else:
            return Formatting.HARMLESS_RESPONSE.value
