import csv
import datetime as dt
import os
import urllib.request
from typing import List

import pandas as pd
from bs4 import BeautifulSoup


class CompanyInfo:
    def __init__(self, company_name, regulator, jurisdiction, date, subject,
                 comments) -> None:
        self.name = company_name
        self.regulator = regulator
        self.jurisdiction = jurisdiction
        self.date = dt.datetime.strptime(date.split("\n")[-1], "%d %b %Y")
        self.subject = subject
        if comments == "No additional comments posted.":
            self.comments = "None"
        else:
            self.comments = comments
            indx = self.comments.find("\tmore\n")
            if indx != -1:
                self.comments = self.comments[:indx]
            self.comments = self.comments.replace("\t", "").replace(
                "\n", "").replace("\r", "")

        self.redirect = None

    def set_redirect(self, redirect_url) -> None:
        self.redirect = redirect_url


class IOSCOParse:
    def __init__(self) -> None:
        self.hard_url = "https://www.iosco.org/investor_protection/?subsection=investor_alerts_portal"
        self.hard_savepoint = 'iosco.html'

    def parse_loop(self) -> List[CompanyInfo]:
        if os.path.isfile(self.hard_savepoint):
            with open(self.hard_savepoint, 'rb') as f:
                html_code = f.read()
            print("READ FROM FILE")
        else:
            with urllib.request.urlopen(self.hard_url) as url_handl:
                # save the html code
                html_code = url_handl.read()
                if not os.path.isfile(self.hard_savepoint):
                    with open(self.hard_savepoint, 'wb') as f:
                        f.write(html_code)

        soup = BeautifulSoup(html_code, "html.parser")
        table_body = soup.find("table", {"id": "tbl_inv_alerts_data"})
        table_entries = table_body.find_all("tr")

        company_list: List[CompanyInfo] = []
        for entry in table_entries[1:]:
            entries = entry.find_all("td")
            lst = [x.text.strip() for x in entries]
            assert len(lst) == 6

            cmp = CompanyInfo(*lst)
            redir = entries[3].find('a').attrs['href']
            cmp.set_redirect(redir)
            company_list.append(cmp)

        return company_list

    @staticmethod
    def to_pandas(comp_list: List[CompanyInfo]) -> pd.DataFrame:
        return pd.DataFrame.from_records([c.__dict__ for c in comp_list])


if __name__ == "__main__":
    p = IOSCOParse()
    cl = p.parse_loop()
    df = IOSCOParse.to_pandas(cl)
    df['index'] = df.index
    df.to_csv("iosco.tsv", sep='\t', quotechar="\'", quoting=csv.QUOTE_NONE)
