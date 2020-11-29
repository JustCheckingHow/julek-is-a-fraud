from data_source import DataSource
import requests
import pandas as pd
import glob
import os
import signal
import asyncio
import signal
import bs4
from modules.RGX_GAME.random_page_rgx import RandomRGXExtractor
import hashlib
import logging
import csv
import pickle
import io

path = "modules/IOSCO/iosco.tsv"
DATA = pd.read_csv(path,
                   sep='\t',
                   quotechar="\'",
                   quoting=csv.QUOTE_NONE,
                   error_bad_lines=False)
DATA['name'] = DATA['name'].astype(str)

pickle_path = "modules/WEBPAGE_RESOLVE/out.pkl"
with open(pickle_path, "rb") as f:
    SCRAPPED = pickle.load(f)

# Mapping na nazwy firm plus szukanie powiązań między firmami z tymi samymi URLami
SCRAPPED = {i: j for i, j in SCRAPPED[1:]}
# SCRAPPED = pd.read_csv(io.StringIO(SCRAPPED))
# SCRAPPED = {}

GLOB_CACHE = pd.read_csv("modules/WEBPAGE_RESOLVE/cache.tsv",
                         error_bad_lines=False,
                         sep='\t',
                         index_col='company')


class WebpageResolver(DataSource):
    DOMAINS = ["biz.pl", "com", "org", "pl", "eu", "net", "co.uk", "hk"]
    CACHE_LOC = "modules/WEBPAGE_RESOLVE/cache.tsv"
    PAGE_CACHE_LOC = "modules/WEBPAGE_RESOLVE/cache/"

    def __init__(self, company_name):
        super().__init__(company_name)
        requests.adapters.DEFAULT_RETRIES = 1

        filt = DATA['name'].apply(lambda x: company_name.lower() in x.lower() if not pd.isna(x) else False)
        data = DATA[filt]

        if len(data) > 0:
            self.company_name = data['name'].values[0]
        try:
            self.cache = pd.read_csv(WebpageResolver.CACHE_LOC,
                                     error_bad_lines=False,
                                     sep='\t',
                                     index_col='company')
        except FileNotFoundError:
            self.cache = pd.DataFrame(columns=['company', 'rank'])
            self.cache = self.cache.set_index('company')

    @staticmethod
    def get_html(webpage, stash=True, only_cached=False):
        page_name = webpage.replace("http://", "")
        page_name = hashlib.md5(page_name.encode('utf-8')).hexdigest()

        all_pages = glob.glob(WebpageResolver.PAGE_CACHE_LOC + "*")

        if "http" not in webpage:
            webpage = "http://" + webpage

        if any(map(lambda x: page_name == os.path.split(x)[-1],
                   all_pages)) or only_cached:
            with open(WebpageResolver.PAGE_CACHE_LOC + page_name, "r") as f:
                return f.read()
        else:
            try:
                return SCRAPPED[webpage]
            except KeyError:
                pass

        try:
            page = requests.get(webpage)
        except (requests.exceptions.SSLError,
                requests.exceptions.ConnectionError):
            return ''
        if stash:
            with open(WebpageResolver.PAGE_CACHE_LOC + page_name,
                      "w",
                      encoding="utf-8") as f:
                f.write(page.text)

        return page.text

    # @staticmethod
    # def get_links_from_page(webpage, stash=True):
    #     html = WebpageResolver.get_html(webpage, stash)
    #     soup = bs4.BeautifulSoup(html, features="lxml")
    #     links = soup.find_all("a", href=True)

    # @staticmethod
    # def _duckduckgo_resolve(webpage):
    #     url = f"https://duckduckgo.com/?q={webpage}&ia=web"

    @staticmethod
    def _find_in_redirect(url, stash=False):
        url = url.lstrip(":").rstrip("/")
        page = WebpageResolver.get_html(url, stash=stash).lower()
        extractor = RandomRGXExtractor()
        data = extractor.parse_webpage(page)
        res = []
        if len(data['website']) > 50:
            return None
        for url in data['website']:
            if 'u.s.' in url:
                continue
            if '.gov' in url or 'finma.ch' in url:
                continue
            if 'http' not in url:
                url = 'http://' + url
            # if WebpageResolver.check_exists(url):
            res.append(url)
            if ".co.uk" in url:
                res.append(url.replace(".co.uk", ".pl"))
            else:
                res.append('.'.join(url.split(".")[:-1]) + ".pl")
        return res

    @staticmethod
    def _desperate_resolve(name):
        logging.info("Desperate URL resolving")
        # if " " not in name:
        #     main_domain = name+".pl"
        #     if WebpageResolver.check_exists(main_domain):
        #         return main_domain
        # else:
        #     main_domain = name.replace(" ", "-")
        #     main_domain += ".pl"
        #     if WebpageResolver.check_exists(main_domain):
        #         return main_domain

        #     main_domain = name.replace(" ", "")
        #     main_domain += ".pl"
        #     if WebpageResolver.check_exists(main_domain):
        #         return main_domain

        # return None
        name = name.lower()
        res = [name + ".pl"]
        main_domain = name.replace(" ", "-")
        main_domain += ".pl"
        res.append(main_domain)
        main_domain = name.replace(" ", "")
        main_domain += ".pl"
        res.append(main_domain)
        return res

    def find_main_domain(self, company_name):
        filt = DATA['name'].apply(lambda x: company_name.lower() in x.lower()
                                  if not pd.isna(x) else False)
        data = DATA[filt]

        res = []
        if len(data) > 0:
            self.company_name = data['name'].values[0]
            if 'www' in data['name'].values[0] or 'http' in data[
                    'name'].values[0]:
                url = data['name'].values[0]
                res.append(url)
                if ".co.uk" in url:
                    res.append(url.replace(".co.uk", ".pl"))
                else:
                    res.append('.'.join(url.split(".")[:-1]) + ".pl")
            else:
                if 'knf.gov.pl' in data['redirect'].values[0]:
                    return None
                url = WebpageResolver._find_in_redirect(
                    data['redirect'].values[0])
                if url is not None:
                    res.extend(url)

        main_domain = WebpageResolver._desperate_resolve(self.company_name)
        res.extend(main_domain)
        return res

    def return_data(self, **kwargs) -> dict:
        if self.company_name.lower() in map(lambda x: x.lower(),
                                            self.cache.index):
            result = self.cache.loc[self.company_name].values[0].split(",")
            return {"webpage": result, "Company Name": self.company_name}

        main_domain = self.find_main_domain(self.company_name)

        if main_domain is None:
            return {'webpage': None, "Company Name": self.company_name}

        results = list(set(main_domain))
        # ending = [i for i in WebpageResolver.DOMAINS if f".{i}" in main_domain or f"{i}." in main_domain]
        # results = WebpageResolver.find_alternative_domains(main_domain, "com")

        self.cache.loc[self.company_name] = ','.join(results)
        self.cache.to_csv(WebpageResolver.CACHE_LOC, sep='\t')
        return {"webpage": results, "Company Name": self.company_name}

    @staticmethod
    def find_alternative_domains(main_domain, ending):
        logging.info("Finding alternative comains")

        tasks = []
        tested = []
        res = []
        for domain in WebpageResolver.DOMAINS:
            webpage = main_domain.replace(ending, domain)

            tested.append(webpage)
            res.append(WebpageResolver.check_exists(webpage))

        answer = filter(lambda x: x[1] is not None, zip(tested, res))
        answer = map(lambda x: x[0], answer)
        return list(answer)

    @staticmethod
    def check_exists(webpage):
        print("Checking", webpage)
        if "http" not in webpage:
            webpage = "http://" + webpage
        try:
            return requests.get(webpage, timeout=10)
        except requests.exceptions.ConnectionError:
            return None
        except requests.exceptions.TooManyRedirects:
            return None

    @staticmethod
    def reverse_search_name(website: str) -> str:
        """
        pass company website, get company name
        or return UNDEFINED
        """
        try:
            return GLOB_CACHE.loc[GLOB_CACHE['rank'].str.contains(website)].index[0]
        except:
            return "UNDEFINED"
