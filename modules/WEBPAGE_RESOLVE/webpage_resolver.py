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


class WebpageResolver(DataSource):
    DOMAINS = ["biz.pl", "com", "org", "pl", "eu", "net", "co.uk", "hk"]
    CACHE_LOC = "modules/WEBPAGE_RESOLVE/cache.tsv"
    PAGE_CACHE_LOC = "modules/WEBPAGE_RESOLVE/cache/"

    def __init__(self, company_name):
        super().__init__(company_name)
        requests.adapters.DEFAULT_RETRIES = 1
        # signal.signal(signal.SIGALRM, None)
        # signal.alarm(2)
        path = "modules/IOSCO/iosco.tsv"
        data = pd.read_csv(path, sep='\t')
        filt = data['name'].apply(lambda x: company_name.lower() in x.lower())
        data = data[filt]

        if len(data) > 0:
            self.company_name = data['name'].values[0]

        try:
            self.cache = pd.read_csv(
                WebpageResolver.CACHE_LOC, sep='\t', index_col='company')
        except FileNotFoundError:
            self.cache = pd.DataFrame(columns=['company', 'rank'])
            self.cache = self.cache.set_index('company')

    @staticmethod
    def get_html(webpage, stash=True):
        page_name = webpage.replace("http://", "")
        page_name = hashlib.md5(page_name.encode('utf-8')).hexdigest()

        all_pages = glob.glob(WebpageResolver.PAGE_CACHE_LOC+"*")
        if any(map(lambda x: page_name == os.path.split(x)[-1], all_pages)):
            with open(WebpageResolver.PAGE_CACHE_LOC+page_name, "r") as f:
                return f.read()

        try:
            page = requests.get(webpage)
        except requests.exceptions.SSLError:
            return ''
        if stash:
            with open(WebpageResolver.PAGE_CACHE_LOC+page_name, "w", encoding="utf-8") as f:
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
        page = WebpageResolver.get_html(url, stash=stash).lower()
        extractor = RandomRGXExtractor()
        data = extractor.parse_webpage(page)
        print(data)
        for url in data['website']:
            if '.gov.' in url or 'finma.ch' in url:
                continue
            if 'http' not in url:
                url = 'http://'+url
            if WebpageResolver.check_exists(url):
                return url

        return None

    @staticmethod
    def _desperate_resolve(name):
        logging.info("Desperate URL resolving")
        if " " not in name:
            main_domain = name+".pl"
            if WebpageResolver.check_exists(main_domain):
                return main_domain
        else:
            main_domain = name.replace(" ", "-")
            main_domain += ".pl"
            if WebpageResolver.check_exists(main_domain):
                return main_domain

            main_domain = name.replace(" ", "")
            main_domain = name+".pl"
            if WebpageResolver.check_exists(main_domain):
                return main_domain

        return None

    def find_main_domain(self, company_name):
        path = "modules/IOSCO/iosco.tsv"
        data = pd.read_csv(path, sep='\t')
        filt = data['name'].apply(lambda x: company_name.lower() in x.lower())
        data = data[filt]

        if len(data) > 0:
            self.company_name = data['name'].values[0]
            if 'www' in data['name'].values[0] or 'http' in data['name'].values[0]:
                return data['name'].values[0]
            else:
                if 'knf.gov.pl' in data['redirect'].values[0]:
                    return None

                url = WebpageResolver._find_in_redirect(
                    data['redirect'].values[0])

                if url is not None:
                    print("URL:", url)
                    return url

        main_domain = WebpageResolver._desperate_resolve(self.company_name)
        return main_domain

    def return_data(self, **kwargs) -> dict:
        if self.company_name.lower() in map(lambda x: x.lower(), self.cache.index):
            result = self.cache.loc[self.company_name].values[0].split(",")
            return {"webpage": result, "Company Name": self.company_name}

        main_domain = self.find_main_domain(self.company_name)

        if main_domain is None:
            return {'webpage': None, "Company Name": self.company_name}

        results = [main_domain]
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
