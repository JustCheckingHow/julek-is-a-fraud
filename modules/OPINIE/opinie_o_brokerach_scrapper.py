import csv
import datetime as dt
import os
import urllib.request
from typing import List

import pandas as pd
from bs4 import BeautifulSoup 


class CompanyOpinions:
    def __init__(self, name, minimal_wage, polish, trading_platforms,
                 demo, CySec_license, FCA_license) -> None:
        
        self.name = name
        self.minimal_wage = minimal_wage
        self.polish = polish
        self.trading_platforms = trading_platforms
        self.demo = demo
        self.CySec_license = CySec_license
        self.FCA_license = FCA_license


class OpinionParser:
    def __init__(self) -> None:
        self.hard_url = 'https://opinie-o-brokerach.pl/'
        self.hard_savepoint = 'opinie.html'


    def _tf_mapping(self, td_element):
        tf_mapping = {'yes': True, 'no': False}
        return tf_mapping[td_element.find('img')['class'][0]]


    def parse_loop(self) -> List[CompanyOpinions]:
        html_code = urllib.request.urlopen(self.hard_url).read()
        
        soup = BeautifulSoup(html_code, 'html.parser')
        table_body = soup.find_all('table')[0]
        table_entries = table_body.find_all('tr')

        company_list: List[CompanyOpinions] = []
        for entry in table_entries[1:]:
            columns = entry.find_all('td')
            assert len(columns) == 7

            aux = {
                'name': columns[0].find('a').text.strip(),
                'minimal_wage': columns[1].text,
                'polish': self._tf_mapping(columns[2]),
                'trading_platforms': columns[3].text,
                'demo': self._tf_mapping(columns[4]),
                'CySec_license': self._tf_mapping(columns[5]),
                'FCA_license': self._tf_mapping(columns[6])
            }

            cmp = CompanyOpinions(**aux)
            company_list += [cmp]

        return company_list


    @staticmethod
    def to_pandas(comp_list: List[CompanyOpinions]) -> pd.DataFrame:
        return pd.DataFrame.from_records([c.__dict__ for c in comp_list])


if __name__ == '__main__':
    p = OpinionParser()
    cl = p.parse_loop()
    df = OpinionParser.to_pandas(cl)
    df['index'] = df.index
    df.to_csv('opinions.tsv', sep='\t', quotechar='\'', escapechar='\\', quoting=csv.QUOTE_NONE)