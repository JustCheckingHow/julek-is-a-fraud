from data_source import DataSource
import pandas as pd
import requests
from modules import WebpageResolver
import bs4
import glob


class AlexaRank(DataSource):
    LOC = "modules/ALEXA_RANK/"
    ALEXA_ROOT = "https://www.alexa.com/siteinfo/"

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
        # if self.company_name in self.cache.index:
        #     rank = self.cache.loc[self.company_name].values[0]
        #     return {"AlexaRank": rank}

        page = requests.get(self.webpage).text

        soup = bs4.BeautifulSoup(page, features="lxml")
        rank = soup.find_all("div", class_="rankmini-rank")[0].text.strip()
        rank = rank.lstrip("#").replace(",","")

        self.cache.loc[self.company_name] = rank
        self.cache.to_csv(AlexaRank.LOC+"cache.tsv", sep='\t')

        return {"AlexaRank": rank}


if __name__ == "__main__":
    resource = AlexaRank("aviva")
    print(resource.return_data())
