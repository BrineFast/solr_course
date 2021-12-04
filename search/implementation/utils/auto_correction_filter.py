from deeppavlov import build_model
from langdetect import detect_langs


class AutoCorrectionFilter():
    def __init__(self):
        self.model_en = build_model(config="ml_configs/en.json", download=True)
        self.model_ru = build_model(config="ml_configs/ru.json", download=True)

    def correct(self, text: str) -> str:
        layout_en: dict = dict(zip(map(ord, '''qwertyuiop[]asdfghjkl;'zxcvbnm,./`QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'''),
                                   '''йцукенгшщзхъфывапролджэячсмитьбю.ёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'''))
        layout_ru: dict = dict(zip(map(ord, '''йцукенгшщзхъфывапролджэячсмитьбю.ёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'''),
                                   '''qwertyuiop[]asdfghjkl;'zxcvbnm,./`QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'''))
        query: str = ""
        for word in text.split():
            if detect_langs(word) == "ru" and self.model_en([word]) > self.model_ru[word]:
                query = query + word.translate(layout_ru)
            elif detect_langs(word) == "en" and self.model_en([word]) < self.model_ru[word]:
                query = query + word.translate(layout_en)
        if query:
            return query
        return text
