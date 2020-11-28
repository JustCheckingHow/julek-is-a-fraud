import csv
from types import CodeType

import pandas as pd
import requests
from tqdm import tqdm

from modules import Scamwatcher, WebpageResolver
from modules.ALEXA_RANK.alexa_rank import AlexaRank
from modules.WHO_IS.whois_api import WhoIs


MAIN_DATA = './modules/IOSCO/iosco.tsv'
KNF_WHITELIST = './modules/KNF/whitelist.csv'
KNF_BLACKLIST = './modules/KNF/blacklist.csv'



with open(KNF_WHITELIST) as f:
    knf_whitelist = f.readlines()[1:]
with open(KNF_BLACKLIST) as f:
    knf_blacklist = f.readlines()[1:]

# print(knf_whitelist)


def run_scrapper():
    df = pd.read_csv(MAIN_DATA, sep='\t', quotechar="\'", quoting=csv.QUOTE_NONE) 
    with tqdm(df['name']) as t:
        for company_name in t:
            t.set_postfix(company_name=company_name)
            try:
                res = WebpageResolver(company_name).return_data()['webpage']
            except (UnicodeError, requests.exceptions.InvalidURL):
                continue

            if res is None:
                continue
            if not isinstance(res, list):
                res = [res]
            for webpage in res:
                if "http" not in webpage:
                    webpage = "http://" + webpage
                try:
                    _ = WebpageResolver.get_html(webpage, stash=True)
                except Exception as e:
                    print(f"Failed for {company_name}: {webpage}")


"""



COOPER MARKETS s.r.o	https://web.coopermarkets.com/
"""
def investigate_company(company) -> dict:
    """
    Check who is 
    """
    

    wi = WhoIs(company)
    ar = AlexaRank(company)
    sw = Scamwatcher(company)
    # knf = 
    result = {
        **wi.return_data()
        **sw.return_data()
        **ar.return_data()
    }



if __name__ == "__main__":
    run_scrapper()
    # investigate_company("COOPER MARKETS s.r.o")