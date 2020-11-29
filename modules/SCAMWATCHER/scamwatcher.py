from data_source import DataSource
import pandas as pd
import requests
from modules import WebpageResolver
import glob
import numpy as np


class Scamwatcher(DataSource):
    LOC = "modules/SCAMWATCHER/"
    PAGE_ROOT = "https://www.scamwatcher.org/{0}-review/"
    BINS = [5000, 30000, 70000]

    def __init__(self, company_name):
        super().__init__(company_name)
        self.company_name = WebpageResolver(company_name).company_name
        try:
            self.cache = pd.read_csv(
                Scamwatcher.LOC+"cache.tsv", sep='\t', index_col='company')
        except FileNotFoundError:
            self.cache = pd.DataFrame(columns=['company', 'rank'])
            self.cache.set_index('company')
            
    def return_data(self, **kwargs) -> dict:
        """ Key: Scamwatcher """
        if self.company_name in self.cache.index:
            data = self.cache.loc[self.company_name, 'rank']
            return {"Scamwatcher": str(data)}

        page = Scamwatcher.PAGE_ROOT.format(self.company_name).replace(" ", "-")
        res = requests.get(page)
        found = "Oops! That page" not in res.text
        if not found:
            page = Scamwatcher.PAGE_ROOT.format(' '.join(self.company_name.split()[:-1])).replace(" ", "-")
            res = requests.get(page)
            found = "Oops! That page" not in res.text

        if not found: 
            page = Scamwatcher.PAGE_ROOT.format(self.company_name.lower().replace("ltd", "limited")).replace(" ", "-")
            print(page)
            res = requests.get(page)
            found = "Oops! That page" not in res.text

        self.cache.loc[self.company_name, 'rank'] = found
        self.cache.to_csv(Scamwatcher.LOC+"cache.tsv", sep='\t')
        return {"Scamwatcher": str(bool(found))}

