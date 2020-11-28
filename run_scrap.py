from types import CodeType
from tqdm import tqdm

from modules import Scamwatcher, WebpageResolver
from modules.ALEXA_RANK.alexa_rank import AlexaRank
from modules.WHO_IS.whois_api import WhoIs


MAIN_DATA = './modules/IOSCO/iosco.tsv'


import csv
import requests

import pandas as pd

df = pd.read_csv(MAIN_DATA, sep='\t', quotechar="\'", quoting=csv.QUOTE_NONE) 
with tqdm(df['name']) as t:
    for company_name in t:
        t.set_postfix(company_name=company_name)
        try:
            res = WebpageResolver(company_name).return_data()['webpage']
        except UnicodeError:
            continue

        if res is None:
            continue
        if not isinstance(res, list):
            res = [res]
        for webpage in res:
            if "http" not in webpage:
                webpage = "http://" + webpage
            try:
                html_source = WebpageResolver.get_html(webpage, stash=True)
            except Exception as e:
                print(f"Failed for {company_name}: {webpage}")
