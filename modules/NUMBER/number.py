from bs4 import BeautifulSoup
from data_source import DataSource
import json
import requests
import csv


class Cache:
    def __init__(self, filename):
        self.filename = filename
        self.delim ='\t'

    def append(self, record):
        with open("{}.tsv".format(self.filename), 'a+') as f:
            writer = csv.writer(f, delimiter=self.delim)
            writer.writerow(record)

    def check_cache(self, key):
        try:
            with open("{}.tsv".format(self.filename)) as f:
                reader = csv.reader(f, delimiter=self.delim)
                for row in reader:
                    if row[0] == key:
                        return row[1]
                return None
        except FileNotFoundError:
            return None


class NumberInfo:
    def __init__(self, number, country, danger=None) -> None:
        self.number = number
        self.country = country
        self.danger = danger


class NumberCheck(DataSource):
    def __init__(self, company_name) -> None:
        super().__init__(company_name)
        self.url = "https://www.nieznanynumer.pl/numer"
        self.cache = Cache("modules/NUMBER/cache")
        # self.cookies = json.load(open("cookies.json", 'r'))

    def check_number(self, number_str):
        print("check_number", number_str)
        n_str = number_str.replace("+", "").replace(" ", "").strip()
        number_query = f"{self.url}/{n_str}"

        cache_check = self.cache.check_cache(self.company_name)
        if cache_check != None:
            nn = NumberInfo()
            nn.number = cache_check[1]
            nn.country = cache_check[2]
            nn.danger = cache_check[3]

            return nn

        webpage = requests.get(
            number_query,
            #    cookies=self.cookies,
            headers={
                'User-Agent': 'Mozilla/5.0'
            }).text
        soup = BeautifulSoup(webpage, "html.parser")
        try:
            country = soup.find("span", {"itemprop": "addressCountry"}).text
        except AttributeError:
            country = "None"
        try:
            danger = soup.find("span", {"id": "progress-bar-inner-text"}).text
        except AttributeError:
            danger = "None"
        
        nbr_dat = NumberInfo(number_str,
                             country=country,
                             danger=danger.replace("%", ""))
        
        self.cache.append([self.company_name, nbr_dat.number, nbr_dat.country, nbr_dat.danger])
        return nbr_dat

    def return_data(self, **kwargs) -> dict:
        return self.check_number(kwargs['number_string']).__dict__
