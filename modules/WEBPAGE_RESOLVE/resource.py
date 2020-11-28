from data_source import DataSource
import requests
import pandas as pd
from requests.adapters import HTTPAdapter

class WebpageResolver(DataSource):
    DOMAINS = [".com", ".org", ".pl", ".eu"]
    CACHE_LOC = "modules/WEBPAGE_RESOLVE/cache.tsv"

    def __init__(self, company_name):
        super().__init__(company_name)
        requests.adapters.DEFAULT_RETRIES = 1
        self.cache = pd.read_csv(WebpageResolver.CACHE_LOC, sep='\t', index_col='company')

    def return_data(self, **kwargs) -> dict:
        if self.company_name in self.cache.index:
            result = self.cache.loc[self.company_name].values[0].split(",")
            return {"webpage": result}
        
        result = []
        for domain in WebpageResolver.DOMAINS:
            try:
                webpage = "http://"+self.company_name+domain
                req = requests.head(webpage, timeout=0.1)
                result.append(webpage)
            except requests.exceptions.ConnectionError:
                pass

        self.cache.loc[self.company_name] = ','.join(result)
        self.cache.to_csv(WebpageResolver.CACHE_LOC, sep='\t')
        return {"webpage": result}

if __name__=="__main__":
    test = WebpageResolver("test")
    print(test.return_data())
