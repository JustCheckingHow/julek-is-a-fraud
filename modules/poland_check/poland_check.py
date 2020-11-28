from modules import WebpageResolver
from data_source import DataSource
from modules import LanguageDetection
import pandas as pd
from bs4 import BeautifulSoup
import bs4
import csv


class PolandCheck(DataSource):
    LOC = "modules/poland_check/"

    def __init__(self, company_name):
        super().__init__(company_name)
        self.websites = WebpageResolver(company_name).return_data()['webpage']
        try:
            self.cache = pd.read_csv(
                PolandCheck.LOC+"cache.tsv", sep='\t', index_col='company')
        except FileNotFoundError:
            self.cache = pd.DataFrame(columns=['company', 'rank'])
            self.cache.set_index('company')

    def return_data(self, **kwargs) -> dict:
        for website in self.websites:
            if '.pl' in website:
                return {"in_poland": True}

        return {"in_poland": self.check_if_polish_text(self.websites)}

    def check_if_polish_text(self, website):
        def tag_visible(element):
            if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
                return False
            if isinstance(element, bs4.element.Comment):
                return False
            return True
        
        def text_from_html(body):
            soup = BeautifulSoup(body, 'html.parser')
            texts = soup.findAll(text=True)
            visible_texts = filter(tag_visible, texts)  
            return u" ".join(t.strip() for t in visible_texts)

        for website in self.websites:
            try:
                text = text_from_html(WebpageResolver.get_html(website))
                ld = LanguageDetection()
                langs = ld.return_data(text=text)
                print(langs, website)
            except:
                continue
            if 'pl' in langs and langs['pl'] > 0.25:
                return True
            return False
        return False


if __name__ == "__main__":
    data = []
    with open("modules/WEBPAGE_RESOLVE/cache.tsv") as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            data.append(row[0])

    for el in data:
        poland_check = PolandCheck(el)
        out = poland_check.return_data()
            
