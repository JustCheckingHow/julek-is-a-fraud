import json
import re
from collections import defaultdict
from typing import List

import bs4
import csv
from numpy.lib.npyio import save
import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import os
import glob


def telephone_normaliser(telpho):
    if len(telpho) < 6:
        return None
    else:
        return telpho


class NumberInfo:
    def __init__(self, number, country, danger=None) -> None:
        self.number = number
        self.country = country
        self.danger = danger


class NumberCheck:
    def __init__(self, company_name) -> None:
        super().__init__(self, company_name)
        self.url = "https://www.nieznanynumer.pl/numer"
        self.cookies = json.load(open("cookies.json", 'r'))

    def check_number(self, number_str):
        n_str = number_str.replace("+", "").replace(" ", "").strip()
        number_query = f"{self.url}/{n_str}"

        webpage = requests.get(number_query,
                               cookies=self.cookies,
                               headers={
                                   'User-Agent': 'Mozilla/5.0'
                               }).text
        soup = BeautifulSoup(webpage, "html.parser")
        try:
            country = soup.find("span", {"itemprop": "addressCountry"}).text
        except AttributeError:
            country = "None"
        try:
            danger = soup.find("div", {"class": "progress-bar-rank4"}).text
        except AttributeError:
            danger = "None"

        nbr_dat = NumberInfo(number_str,
                             country=country,
                             danger=danger.replace("%", ""))
        return nbr_dat

    def return_data(self, **kwargs) -> dict:
        return self.check_number(kwargs['number_string']).__dict__


class RandomRGXExtractor:
    def __init__(self) -> None:
        self.regexes = {
            'phone':
            re.compile(r"[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*"),
            'phone2':
            re.compile(r"\(?([0-9]{3})\)?([ .-]?)([0-9]{3})\2([0-9]{4})/"),
            'email':
            re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"),
            'website':
            re.compile(r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+")
        }

    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, bs4.element.Comment):
            return False
        return True

    def text_from_html(self, body) -> str:
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)  
        return u" ".join(t.strip() for t in visible_texts)


    def download_websites(self,
                          df_fn: str,
                          savedir: str = "../webpages") -> None:
        """
        Download all the websites first, using a IOSCO .tsv 
        The savename IS THE INDEX OF THE ENTRY from the .TSV!
        """
        df = pd.read_csv(df_fn,
                         sep='\t',
                         quotechar="\'",
                         quoting=csv.QUOTE_NONE)

        hdr = {
            'User-Agent': 'Mozilla/5.0',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        os.makedirs(savedir, exist_ok=True)
        for (index, webpage) in zip(df['index'], df['redirect']):
            fn = os.path.join(savedir, f"{index}.html")
            req = urllib.request.Request(webpage, headers=hdr)
            try:
                with urllib.request.urlopen(req) as url_handl:
                    html_code = url_handl.read()
                    with open(fn, 'wb') as f:
                        f.write(html_code)
            except Exception as e:
                print(e)
                print(f"\t{index} Failed to extract {webpage}")

    def parse_webpage(self, html_code=None) -> List[str]:
        text = self.text_from_html(html_code)
        res = defaultdict(list)
        for rgx_name, rgx in self.regexes.items():
            results = re.findall(rgx, text)
            for r in results:
                if 'phone' in rgx_name:
                    n = telephone_normaliser(r)
                    if n:
                        res[rgx_name].append(n)
                else:
                    res[rgx_name].append(r)
        return res

    def extract_wepages(self, webpage_dir: str) -> pd.DataFrame:
        """
        Extract data from the webpage using predefined regex
        """
        webpage_results = defaultdict(list)

        for fn in glob.iglob(os.path.join(webpage_dir, "*.html")):
            indx = int(os.path.basename(fn).replace(".html", ""))
            res = self.parse_webpage(fn)
            webpage_results['index'].append(indx)
            for rn, rv in res.items():
                webpage_results[rn].append(rv)

        return pd.DataFrame.from_dict(webpage_results)


if __name__ == "__main__":
    rg = RandomRGXExtractor()
    # rg.download_websites("./IOSCO/iosco.tsv")
    rg.extract_wepages('../webpages').to_csv("metadata.tsv",
                                             sep='\t',
                                             quotechar="\'",
                                             quoting=csv.QUOTE_NONE)
