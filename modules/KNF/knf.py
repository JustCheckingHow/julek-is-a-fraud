from numpy.lib.function_base import blackman
from data_source import DataSource
import Levenshtein as lv

MAIN_DATA = 'modules/IOSCO/iosco.tsv'
KNF_WHITELIST = 'modules/KNF/whitelist.csv'
KNF_BLACKLIST = 'modules/KNF/blacklist.csv'

with open(KNF_WHITELIST, 'r', encoding='utf-8') as f:
    knf_whitelist = f.read().split("\n")
with open(KNF_BLACKLIST, 'r', encoding='utf-8') as f:
    knf_blacklist = f.read().split("\n")

SUFFIXES = [
    " sp. z o.o.", " sp. k.", " sa", " ltd", " s.l.", " s.c.", " llc",
    " sp. z o. o.", " s.a"
]


def process_list(knf_list):
    return_list = []
    for kw in knf_list:
        kwx = kw.lower().replace("\"", "").replace("\n", "")
        for s in SUFFIXES:
            kwx = kwx.replace(s, "")
        return_list.append(kwx)
    return return_list


knf_whitelist_end = process_list(knf_whitelist)
knf_blacklist_end = process_list(knf_blacklist)


class KNFCheck(DataSource):
    LOC = "modules/KNF/"

    def __init__(self, company_name):
        super().__init__(company_name)
        self.cleaned_company_name = self.company_name.lower()
        for s in SUFFIXES:
            self.cleaned_company_name = self.cleaned_company_name.replace(
                s, "")

    def naive_search(self, knf_list):
        top_matches = []
        for sub in knf_list:
            if self.cleaned_company_name in sub:
                top_matches.append(sub)
        return top_matches

    def checkKNF_list(self, knf_list):
        dist = [lv.distance(self.cleaned_company_name, x) for x in knf_list]
        l1, l2 = zip(*sorted(zip(dist, knf_list), reverse=False))
        return l1, l2

    def __calculate_KNF_score(self, whitelist, blacklist):
        cclen = len(self.cleaned_company_name)
        whitescore, blackscore = 0.0, 0.0
        for score, whitelist_dom in whitelist:
            wlen = len(whitelist_dom)
            whitescore += score / (wlen + cclen)
        for score, blacklist_dom in blacklist:
            blen = len(blacklist_dom)
            blackscore += score / (blen + cclen)
        return {
            "KNF_whitelist_score": whitescore,
            "KNF_blacklist_score": blackscore,
            'top_white': [x[1] for x in whitelist],
            'top': [x[1] for x in blacklist]
        }

    def return_data(self, **kwargs) -> dict:
        top_matches_bl = self.naive_search(knf_blacklist_end)
        top_matches_wl = self.naive_search(knf_whitelist_end)
        if top_matches_bl:
            bl1, bl2 = self.checkKNF_list(top_matches_bl)
            black_list_most_sim = list(zip(bl1, bl2))
        else:
            black_list_most_sim = []
        if top_matches_wl:
            wl1, wl2 = self.checkKNF_list(top_matches_wl)
            white_list_most_sim = list(zip(wl1, wl2))
        else:
            white_list_most_sim = []

        return self.__calculate_KNF_score(white_list_most_sim,
                                          black_list_most_sim)


if __name__ == "__main__":
    pass
