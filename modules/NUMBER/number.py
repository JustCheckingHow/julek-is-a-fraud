from bs4 import BeautifulSoup
from data_source import DataSource
import json
import requests


class NumberInfo:
    def __init__(self, number, country, danger=None) -> None:
        self.number = number
        self.country = country
        self.danger = danger


class NumberCheck(DataSource):
    def __init__(self, company_name) -> None:
        super().__init__(company_name)
        self.url = "https://www.nieznanynumer.pl/numer"
        # self.cookies = json.load(open("cookies.json", 'r'))

    def check_number(self, number_str):
        n_str = number_str.replace("+", "").replace(" ", "").strip()
        number_query = f"{self.url}/{n_str}"

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
            danger = soup.find("div", {"class": "progress-bar-rank4"}).text
        except AttributeError:
            danger = "None"
        
        nbr_dat = NumberInfo(number_str,
                             country=country,
                             danger=danger.replace("%", ""))
        return nbr_dat

    def return_data(self, **kwargs) -> dict:
        return self.check_number(kwargs['number_string']).__dict__
