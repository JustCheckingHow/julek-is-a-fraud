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
        self.cache = pd.read_csv(
            Scamwatcher.LOC+"cache.tsv", sep='\t', index_col='company')
            
    def return_data(self, **kwargs) -> dict:
        """ Key: Scamwatcher """
        if self.company_name in self.cache.index:
            data = self.cache.loc[self.company_name, 'rank']
            return {"Scamwatcher": data}

        page = Scamwatcher.PAGE_ROOT.format(self.company_name)
        res = requests.get(page)
        found = "Oops! That page" not in res.text
        self.cache.loc[self.company_name, 'rank'] = found
        self.cache.to_csv(Scamwatcher.LOC+"cache.tsv", sep='\t')
        return {"Scamwatcher": found}

