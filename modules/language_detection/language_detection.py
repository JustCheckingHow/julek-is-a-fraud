from data_source import DataSource
from langdetect import detect_langs

class LanguageDetection(DataSource):
    def __init__(self):
        super().__init__(None)

    def return_data(self, **kwargs) -> dict:
        retard_format = detect_langs(kwargs['text'])
        out_dict = {}
        for l in retard_format:
            out_dict[l.lang] = l.prob

        return out_dict

if __name__ == "__main__":
    ld = LanguageDetection()
    data = ld.return_data(text="Alicja ma koteczka")
    print(data)

