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
        pattern = re.compile(r"^Epoch \d*/\d*$")
        return pattern.match(s) is not None

    @staticmethod
    def is_progress_output(s: str) -> bool:
        pattern = r"\[[.>=]*\]"
        return re.search(pattern, s) is not None

    @staticmethod
    def _remove_start_symbols_from(s: str) -> str:
        match = re.search(r"[0-9]", s)
        return s[match.start():] if match else s

    @staticmethod
    def _break_into_separated_lines(s: str) -> str:
        return "\n".join(s.split("-"))

    @staticmethod
    def manipulate_to_show(s: str):
        result = s[:]

        if not TensorflowOutputHelper.is_epoch_indicator(s):
            result = TensorflowOutputHelper._remove_start_symbols_from(s)

        for word, replacement in words_and_replacements.items():
            result = result.replace(word, replacement)

        return TensorflowOutputHelper._break_into_separated_lines(result)
