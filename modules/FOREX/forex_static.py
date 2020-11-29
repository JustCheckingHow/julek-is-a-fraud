import urllib.request
import pandas as pd
import os
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json

"""
{
    "company": ...,
    "org": ...,
    "warning": ...,
    "webiste": ...,
    "date": ...
}
"""

class ForexTable:
    def __init__(self) -> None:
        self.hard_url = f'https://forexrev.pl/lista-ostrzezen/'
        self.save_dir = 'cache'
        os.makedirs(self.save_dir, exist_ok=True)

    def parse_all_pages(self):
        for page_no in range(1,2):
            page = f"{self.hard_url}/?lpage={page_no}"
            fn = os.path.join(self.save_dir, str(page_no) + ".html")
            if not os.path.isfile(fn):
                req = Request(page, headers={'User-Agent': 'Mozilla/5.0'})
                html_code = urlopen(req).read()
                with open(fn, 'wb') as f:
                    f.write(html_code)
            else:
                html_code = open(fn, 'rb').read()

            soup = BeautifulSoup(html_code, 'html.parser')

            table_data = soup.findAll("script")
            print(len(table_data))
            companies = []
            for table in table_data:
                val = table.string

                if val and 'svtPublic' in val:
                    company = {}
                    for line in val.split(";"):
                        if 'data' in line:
                            # print(line)
                            val = line.split("=")[-1].replace(
                                "<span>", "").replace("</span>",
                                                      "").replace("\'",
                                                                  "").strip()
                            company['date'] = val
                        elif 'nazwa_podmiotu' in line:
                            line = line.replace(
                                '<i class="fa fa-chevron-down"></i>', "")
                            val = line.split("=")[-1].replace("\'", "").strip()
                            company['org'] = val.encode('ascii', 'replace').decode("utf-8")
                        elif 'spolka' in line:
                            val = line.split("=")[-1].replace("\'", "").strip()
                            company['company'] = val.encode('ascii', 'ignore').decode("utf-8")
                        elif 'strona_www' in line:
                            val = line.split("=")[-1]
                            company['website'] = val.replace("\'", "").strip()
                        elif 'organ_wydajacy_ostrzezenie' in line:
                            val = line.split("['organ_wydajacy_ostrzezenie'] = ")[-1]
                            s = BeautifulSoup(val, 'html.parser').find('a')
                            if s is not None:
                                company['warning'] = s.text.strip()
                            else:
                                company['warning'] = None
                            companies.append(company)
                            company = {}

                    # break
            # break
            print(len(companies))
            json.dump(companies, open("all_companies.json", 'w'))

if __name__ == "__main__":
    ft = ForexTable()
    ft.parse_all_pages()