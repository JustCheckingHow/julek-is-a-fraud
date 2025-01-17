import re
from collections import defaultdict
from typing import List

import bs4
import csv
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import os
import glob


def telephone_normaliser(telpho):
    #disable dates with / separator
    # add more
    date_regex = re.compile(r"(?:(19|20)\d\d[- \/.](0[1-9]|1[012])[- \/.](0[1-9]|[12][0-9]|3[01]))|(?:(0[1-9]|[12][0-9]|3[01])[- \/.](0[1-9]|1[012])[- \/.](19|20)\d\d)")
    res = re.findall(date_regex, telpho)
    if len(res) > 0:
        return None
    telpho = telpho.replace(" ", "")
    if len(telpho) < 7:
        return None
    else:
        return telpho

def website_normaliser(url):
    url = url.replace(" ", "")
    try:
        float(url)
        return None
    except:
        pass
    if len(url) < 4:
        return None
    else:
        return url

class RandomRGXExtractor:
    def __init__(self) -> None:
        self.regexes = {
            'phone1':
            re.compile(r"[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*"),
            'email':
            re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"),
            'website':
            re.compile(r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"),
            'phone':
            re.compile(
                r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'),
            'phone-polish':
            re.compile(
                r'(?:(?:(?:\+|00)?48)|(?:\(\+?48\)))?(?:1[2-8]|2[2-69]|3[2-49]|4[1-68]|5[0-9]|6[0-35-9]|[7-8][1-9]|9[145])\d{7}'
            )
        }
        # drop dates: (19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])

    def tag_visible(self, element):
        if element.parent.name in [
                'style', 'script', 'head', 'title', 'meta', '[document]'
        ]:
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
                    if n is not None:
                        res[rgx_name].append(n)
                elif 'website' in rgx_name:
                    w = website_normaliser(r)
                    if w is not None:
                        res[rgx_name].append(w)
                else:
                    res[rgx_name].append(r)
        # print(res)
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
