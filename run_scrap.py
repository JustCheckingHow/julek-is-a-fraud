from collections import defaultdict
import csv
import numpy as np
import pandas as pd
import requests
from tqdm import tqdm
import Levenshtein as lv
from modules import Scamwatcher, WebpageResolver
from modules.ALEXA_RANK.alexa_rank import AlexaRank
from modules.WHO_IS.whois_api import WhoIs
from modules.KNF.knf import KNFCheck
import json

MAIN_DATA = './modules/IOSCO/iosco.tsv'


def run_scrapper():
    df = pd.read_csv(MAIN_DATA,
                     sep='\t',
                     quotechar="\'",
                     quoting=csv.QUOTE_NONE)
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


def investigate_company(company) -> dict:
    """
    Get info about the company
    """
    wi = WhoIs(company)
    ar = AlexaRank(company)
    sw = Scamwatcher(company)
    kfc = KNFCheck(company)

    result = {
        **kfc.return_data(),
        **wi.return_data(),
        **ar.return_data(),
        **sw.return_data()
    }
    return result


def iterate_over_companies(source_fn):
    source_df = pd.read_csv(source_fn, sep="\t")

    result_df = defaultdict(list)
    for company, _ in tqdm(zip(source_df['company'], source_df['rank'])):
        result = investigate_company(company=company)
        result_df['company'].append(company)
        result_df['rank'].append(company)
        for r in result:
            result_df[r].append(result[r])

    df = pd.DataFrame.from_dict(result_df)
    df.to_csv("final.csv", sep=';', index=False)


if __name__ == "__main__":
    pass
    # run_scrapper()
    res = investigate_company("Wantuch")
    print(res)
    # iterate_over_companies("cache.tsv")