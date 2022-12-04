import re


words_and_replacements = {
    "Epoch": "Época",
    "accuracy": "acurácia",
    "loss": "perda",
    "precision": "precisão"
}


class TensorflowOutputHelper:
    @staticmethod
    def is_epoch_indicator(s: str) -> bool:
        pattern = re.compile(r"^(Epoch|Época)\s\d*/\d*$")
        return pattern.match(s) is not None

    @staticmethod
    def is_training_output(s: str) -> bool:
        keys = filter(lambda k: k != "Epoch", words_and_replacements.keys())
        return all(key in s for key in keys)

    @staticmethod
    def _remove_start_symbols_from(s: str) -> str:
        match = re.search(r"[0-9]", s)

        if match:
            return s[match.start():]

        return s

    @staticmethod
    def _break_things_into_separated_lines(s: str) -> str:
        slices = s.split('-')
        result = ""

        if slices:
            for slice in slices:
                result += slice + '\n'

        return result

    @staticmethod
    def manipulate_to_show(s: str):
        result = s[:]

        if not TensorflowOutputHelper.is_epoch_indicator(s):
            result = TensorflowOutputHelper._remove_start_symbols_from(s)

        for word, replacement in words_and_replacements.items():
            result = result.replace(word, replacement)

        return TensorflowOutputHelper._break_things_into_separated_lines(result)
