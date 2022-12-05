import re

words_and_replacements = {
    "Epoch": "Época",
    "accuracy": "acurácia",
    "loss": "perda",
    "precision": "precisão",
    "step": "etapa",
    "ETA": "Tempo estimado de término",
}


class TensorflowOutputHelper:
    @staticmethod
    def is_epoch_indicator(s: str) -> bool:
        """ Check if tensorflow output is an epoch indicator """
        pattern = re.compile(r"^Epoch \d*/\d*$")
        return pattern.match(s) is not None

    @staticmethod
    def is_progress_output(s: str) -> bool:
        """ Check if tensorflow output is a progress indicator with metrics """
        pattern = r"\[[.>=]*\]"
        return re.search(pattern, s) is not None

    @staticmethod
    def _remove_start_symbols_from(s: str) -> str:
        """ Remove weird symbols until find a number """
        match = re.search(r"[0-9]", s)
        return s[match.start():] if match else s

    @staticmethod
    def _break_into_separated_lines(s: str) -> str:
        return "\n".join(s.split("-"))

    @staticmethod
    def manipulate_to_show(s: str):
        """
        Translate some words on tensorflow output and 
        remove undesired symbols from progress indicator
        """

        result = s[:]

        if not TensorflowOutputHelper.is_epoch_indicator(s):
            result = TensorflowOutputHelper._remove_start_symbols_from(s)

        for word, replacement in words_and_replacements.items():
            result = result.replace(word, replacement)

        return TensorflowOutputHelper._break_into_separated_lines(result)
