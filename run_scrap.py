from collections import defaultdict
import csv
from modules.FOREX.forex import ForexReview
import numpy as np
import pandas as pd
import requests
from tqdm import tqdm
import Levenshtein as lv
from modules import Scamwatcher, WebpageResolver
from modules.ALEXA_RANK.alexa_rank import AlexaRank
from modules.WHO_IS.whois_api import WhoIs
from modules.KNF.knf import KNFCheck
from modules.NUMBER.number import NumberCheck
from modules.TFIDF.analyser import TFNeighbour
import json

MAIN_DATA = './modules/IOSCO/iosco.tsv'


def run_scrapper():
    df = pd.read_csv(MAIN_DATA,
                     sep='\t',
                     quotechar="\'",
                     error_bad_lines=False,
                     quoting=csv.QUOTE_NONE)
    with tqdm(df['name'].iloc[667 + 753 + 4099:]) as t:
        for company_name in t:
            t.set_postfix(company_name=company_name)
            try:
                res = WebpageResolver(company_name).return_data()['webpage']
            except (UnicodeError, requests.exceptions.InvalidURL,
                    requests.exceptions.MissingSchema, AttributeError,
                    requests.exceptions.ConnectionError):
                continue

            # if res is None:
            #     continue
            # if not isinstance(res, list):
            #     res = [res]
            # for webpage in res:
            #     if "http" not in webpage:
            #         webpage = "http://" + webpage
            #     try:
            #         _ = WebpageResolver.get_html(webpage, stash=True)
            #     except Exception as e:
            #         print(f"Failed for {company_name}: {webpage}")


def investigate_company(company) -> dict:
    """
    Get info about the company
    """
    wi = WhoIs(company)
    ar = AlexaRank(company)
    sw = Scamwatcher(company)
    kfc = KNFCheck(company)
    fx = ForexReview(company)
    result = {
        **kfc.return_data(),
        **wi.return_data(),
        **ar.return_data(),
        **sw.return_data(),
        **fx.return_data()
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
    # run_scrapper()
    # for num in ['+48661512422', '48225788692', '48221043705']:
    #     nc = NumberCheck('blackrock')
    #     print(nc.return_data(number_string=num))


    INDEX_LOC = "modules/TFIDF/pca_index.json"
    index_set = json.load(open(INDEX_LOC, 'r'))
    index_set = {int(k): v for k, v in index_set.items()}
    inverse_indx = {v: k for k, v in index_set.items()}

    for company in inverse_indx:
        tf = TFNeighbour(company)
        print(tf.return_data())