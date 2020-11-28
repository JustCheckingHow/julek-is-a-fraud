from data_source import DataSource
import pandas as pd
import requests
from modules import WebpageResolver
import bs4
import glob
import numpy as np


class AlexaRank(DataSource):
    LOC = "modules/ALEXA_RANK/"
    ALEXA_ROOT = "https://www.alexa.com/siteinfo/"
    BINS = [5000, 30000, 70000]

    def __init__(self, company_name):
        super().__init__(company_name)
        self.cache = pd.read_csv(
            AlexaRank.LOC+"cache.tsv", sep='\t', index_col='company')
        try:
            res = WebpageResolver(company_name).return_data()['webpage']
            self.webpage = res[0]
        except IndexError as e:
            print("WEBPAGE NOT FOUND")
            raise e

    def return_data(self, **kwargs) -> dict:
        """ Returns Alexa Rank score in 0-4 scale.
             0 - high
             1 - moderate 
             2 - low
             3 - very low
             4 - not indexed
        """
        if self.company_name in self.cache.index:
            result = self.cache.loc[self.company_name].values[0]
            return {"AlexaRank": result}

        page = WebpageResolver.get_html(AlexaRank.ALEXA_ROOT+self.webpage, stash=False)

        try:
            soup = bs4.BeautifulSoup(page, features="lxml")
            rank = soup.find_all("div", class_="rankmini-rank")[0].text.strip()
            rank = int(rank.lstrip("#").replace(",",""))

            rank = np.digitize(rank, AlexaRank.BINS)
            self.cache.loc[self.company_name] = rank
            self.cache.to_csv(AlexaRank.LOC+"cache.tsv", sep='\t')
            return {"AlexaRank": rank}
        except IndexError:
            # The page is so small that it's not even indexed in Alexa
            return {"AlexaRank": 4}


if __name__ == "__main__":
    resource = AlexaRank("scamwatcher")
    print(resource.return_data())
