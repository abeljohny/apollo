from Dbias.bias_classification import classifier

from constants import BiasIndicators, Formatting


class Bias:
    def __init__(self):
        pass

    @staticmethod
    def classify_bias(text: str):
        """Computes and returns how biased a string is"""
        return classifier(text)

    @staticmethod
    def print_classify_bias(text: str) -> str:
        bias_score = Bias.classify_bias(text)
        if bias_score[0]["label"] == BiasIndicators.BIASED.value:
            return Formatting.BIASED_RESPONSE.value.format(
                score=f"{bias_score[0]['score']:.2%}"
            )
        else:
            return Formatting.UNBIASED_RESPONSE.value.format(
                score=f"{bias_score[0]['score']:.2%}"
            )
