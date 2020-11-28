from modules import WebpageResolver
from data_source import DataSource
from modules import LanguageDetection
import pandas as pd

class PolandCheck(DataSource):
    LOC = "modules/poland_check/"

    def __init__(self, company_name):
        super().__init__(company_name)
        self.websites = WebpageResolver(company_name).return_data()['webpage']
        try:
            self.cache = pd.read_csv(
                PolandCheck.LOC+"cache.tsv", sep='\t', index_col='company')
        except FileNotFoundError:
            self.cache = pd.DataFrame(columns=['company', 'rank'])
            self.cache.set_index('company')

    def return_data(self, **kwargs) -> dict:
        for website in self.websites:
            if '.pl' in website:
                return {"in_poland": True}

        return {"in_poland": False}
