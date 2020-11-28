from data_source import DataSource
import requests
import pandas as pd
import glob
import os


class WebpageResolver(DataSource):
    DOMAINS = [".com", ".org", ".pl", ".eu"]
    CACHE_LOC = "modules/WEBPAGE_RESOLVE/cache.tsv"
    PAGE_CACHE_LOC = "modules/WEBPAGE_RESOLVE/cache/"

    def __init__(self, company_name):
        super().__init__(company_name)
        requests.adapters.DEFAULT_RETRIES = 1
        self.cache = pd.read_csv(WebpageResolver.CACHE_LOC, sep='\t', index_col='company')

    @staticmethod
    def get_html(webpage):
        page_name = webpage.replace("http://", "")

        all_pages = glob.glob(WebpageResolver.PAGE_CACHE_LOC+"*")
        if any(map(lambda x: page_name == os.path.split(x)[-1], all_pages)):
            with open(WebpageResolver.PAGE_CACHE_LOC+page_name, "r") as f:
                return f.read()

        page = requests.get(webpage)
        with open(WebpageResolver.PAGE_CACHE_LOC+page_name, "w") as f:
            f.write(page.text)
        
        return page.text

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
    res = test.return_data()
    print(res)
    print(WebpageResolver.get_html(res['webpage'][0]))
