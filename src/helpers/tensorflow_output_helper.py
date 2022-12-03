import re


words_and_replacements = {
    "Epoch": "Época",
    "accuracy": "acurácia",
    "loss": "perda",
}


class TensorflowOutputHelper:
    @staticmethod
    def is_epoch_indicator(s: str):
        return "Epoch" in s or "Época" in s

    @staticmethod
    def _remove_start_symbols_from(s: str):
        match = re.search(r"[0-9]", s)

        if match:
            return s[match.start():]

        return s

    @staticmethod
    def manipulate_to_show(s: str):
        result = s[:]

        if not TensorflowOutputHelper.is_epoch_indicator(s):
            result = TensorflowOutputHelper._remove_start_symbols_from(s)

        for word, replacement in words_and_replacements.items():
            result = result.replace(word, replacement)

        return result
