import csv
import numpy as np
import pandas as pd
import requests
from tqdm import tqdm
from pyjarowinkler import distance
import Levenshtein as lv
from modules import Scamwatcher, WebpageResolver
from modules.ALEXA_RANK.alexa_rank import AlexaRank
from modules.WHO_IS.whois_api import WhoIs

from pyjarowinkler import distance

MAIN_DATA = './modules/IOSCO/iosco.tsv'
KNF_WHITELIST = './modules/KNF/whitelist.csv'
KNF_BLACKLIST = './modules/KNF/blacklist.csv'

with open(KNF_WHITELIST) as f:
    knf_whitelist = f.readlines()[1:]
with open(KNF_BLACKLIST) as f:
    knf_blacklist = f.readlines()[1:]

suffixes = [
    "sp. z o.o.", "sp. k.", "sa", "ltd", "s.l.", "s.c.", "llc", "sp. z o. o."
]
knf_whitelist_end, knf_blackslist_end = [], []
for kw, kb in zip(knf_whitelist, knf_blacklist):
    kwx = kw.lower().replace("\n", "").replace("\"", "")
    kbx = kb.lower().replace("\n", "").replace("\"", "")
    for s in suffixes:
        kwx = kwx.replace(s, "")
        kbx = kbx.replace(s, "")

    knf_blackslist_end.append(kbx)
    knf_whitelist_end.append(kwx)


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


"""
COOPER MARKETS s.r.o	https://web.coopermarkets.com/
"""


def naive_search(company_name, knf_list):
    cmp = company_name.lower()
    for s in suffixes:
        cmp = cmp.replace(s, "")
    # top_matches = [company_name in x for x in knf_list]
    top_matches = []
    for sub in knf_list:
        if cmp in sub:
            top_matches.append(sub)
    print(top_matches)
    return top_matches


def checkKNF_list(company_name, knf_list):
    dist = [lv.distance(company_name, x) for x in knf_list]
    l1, l2 = zip(*sorted(zip(dist, knf_list), reverse=False))
    return l1, l2


def investigate_company(company) -> dict:
    """
    
    """
    wi = WhoIs(company)
    ar = AlexaRank(company)
    sw = Scamwatcher(company)

    top_matches_bl = naive_search(company, knf_blackslist_end)
    top_matches_wl = naive_search(company, knf_whitelist_end)

    if top_matches_bl:
        bl1, bl2 = checkKNF_list(company, top_matches_bl)
        black_list_most_sim = list(zip(bl1, bl2))
    else:
        black_list_most_sim = None
    if top_matches_wl:
        wl1, wl2 = checkKNF_list(company, top_matches_wl)
        white_list_most_sim = list(zip(wl1, wl2))
    else:
        white_list_most_sim = None
    result = {
        'whitelist': white_list_most_sim,
        'blacklist': black_list_most_sim,
        **wi.return_data(),
        **ar.return_data(),
        **sw.return_data()
    }

    return result


if __name__ == "__main__":
    pass
    # run_scrapper()
    res = investigate_company("Wantuch")
    print(res)