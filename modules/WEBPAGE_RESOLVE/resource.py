from data_source import DataSource
import requests
import pandas as pd

class WebpageResolver(DataSource):
    DOMAINS = [".com", ".org"]

    def __init__(self, companyName):
        super().__init__(companyName)
        self.cache = pd.read_csv("modules/WEBPAGE_RESOLVE/cache.tsv", sep='\t')

    def return_data(self, **kwargs) -> dict:
        return requests.get("wp.pl")

if __name__=="__main__":
    test = WebpageResolver("test")
