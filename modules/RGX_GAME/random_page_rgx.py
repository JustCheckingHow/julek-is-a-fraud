from collections import defaultdict
import bs4
import re
from typing import List


def telephone_normaliser(telpho):
    if len(telpho) < 6:
        return None
    else:
        return telpho


class RandomRGXExtractor:
    def __init__(self) -> None:
        self.regexes = {
            'phone':
            re.compile(r'[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*'),
            'phone2':
            re.compile(r'\(?([0-9]{3})\)?([ .-]?)([0-9]{3})\2([0-9]{4})/'),
            'email':
            re.compile(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$'),
            'website':
            re.compile(r'(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+')
        }

    def parse_webpage(self) -> List[str]:
        with open('test.html', 'r') as f:
            html_code = f.read()

        soup = bs4.BeautifulSoup(html_code, "html.parser")
        paragraphs = soup.find_all("p")

        res = defaultdict(list)
        for p in paragraphs:
            ptext = p.text.strip()
            for rgx_name, rgx in self.regexes.items():
                results = re.findall(rgx, ptext)
                for r in results:
                    if 'phone' in rgx_name:
                        n = telephone_normaliser(r)
                        if n:
                            res[rgx_name].append(n)
                    else:
                        res[rgx_name].append(r)
        print(res)


if __name__ == "__main__":
    rg = RandomRGXExtractor()
    rg.parse_webpage()