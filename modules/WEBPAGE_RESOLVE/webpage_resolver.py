from data_source import DataSource
import grequests
import requests
import pandas as pd
import glob
import os
import signal
import asyncio
import signal
import bs4


class WebpageResolver(DataSource):
    DOMAINS = [".com", ".org", ".pl", ".eu", ".net", ".co.uk"]
    CACHE_LOC = "modules/WEBPAGE_RESOLVE/cache.tsv"
    PAGE_CACHE_LOC = "modules/WEBPAGE_RESOLVE/cache/"

    def __init__(self, company_name):
        super().__init__(company_name)
        requests.adapters.DEFAULT_RETRIES = 1
        # signal.signal(signal.SIGALRM, None)
        # signal.alarm(2)

        try:
            self.cache = pd.read_csv(
                WebpageResolver.CACHE_LOC, sep='\t', index_col='company')
        except FileNotFoundError:
            self.cache = pd.DataFrame(columns=['company', 'rank'])
            self.cache = self.cache.set_index('company')

    @staticmethod
    def get_html(webpage, stash=True):
        page_name = webpage.replace("http://", "")

        all_pages = glob.glob(WebpageResolver.PAGE_CACHE_LOC+"*")
        if any(map(lambda x: page_name == os.path.split(x)[-1], all_pages)):
            with open(WebpageResolver.PAGE_CACHE_LOC+page_name, "r") as f:
                return f.read()

        page = requests.get(webpage)
        if stash:
            with open(WebpageResolver.PAGE_CACHE_LOC+page_name, "w", encoding="utf-8") as f:
                f.write(page.text)

        return page.text

    @staticmethod
    def get_links_from_page(webpage, stash=True):
        html = WebpageResolver.get_html(webpage, stash)
        soup = bs4.BeautifulSoup(html, features="lxml")
        links = soup.find_all("a", href=True)

    def return_data(self, **kwargs) -> dict:
        if self.company_name in self.cache.index:
            result = self.cache.loc[self.company_name].values[0].split(",")
            return {"webpage": result}

        result = self.find_domains()
        self.cache.loc[self.company_name] = ','.join(result)
        self.cache.to_csv(WebpageResolver.CACHE_LOC, sep='\t')
        return {"webpage": result}

    def find_domains(self):
        tasks = []
        tested = []
        for domain in WebpageResolver.DOMAINS:
            webpage = "http://"+self.company_name+domain
            tested.append(webpage)
            tasks.append(self.check_exists(webpage))

        res = grequests.map(tasks, exception_handler=None)
        answer = filter(lambda x: x[1] is not None, zip(tested, res))
        answer = map(lambda x: x[0], answer)
        return list(answer)

    def check_exists(self, webpage):
        return grequests.get(webpage)
