from data_source import DataSource
from modules import WebpageResolver, TaxHeaven
import whois
import signal
import csv
import sys
import bs4
import re
from collections import defaultdict


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


class WhoIs(DataSource):
    def __init__(self, company_name):
        self.regexes = {
            'country': re.compile(r'registrant state\/province: ([^\s]*)'),
            'name': re.compile(r'registrant name: ([^\s]*)'),
            'phone': re.compile(r'registrant phone: ([^\s]*)'),
            'creation_date': re.compile(r'creation date: ([^\s]*)'),
            'registration_date': re.compile(r'registered on: ([^\s]*)')
        }

        super().__init__(None)
        self.tax_havens = TaxHeaven().return_data()['tax_heaven']
        self.cache = Cache('modules/WHO_IS/cache')
        try:
            res = WebpageResolver(company_name).return_data()['webpage']
            self.webpages = res
        except IndexError as e:
            print("WEBPAGE NOT FOUND")
            raise e

    def return_data(self, **kwargs) -> dict:
        out_arr = []
        for uri_with_http in self.webpages:
            uri = uri_with_http.replace('http://', '').replace('https://', '')
            if uri[-1] == "/" or uri[-1] == '.':
                uri = uri[:-1]
            # cache_resp = self.cache.check_cache(uri)
            cache_resp = None
            if cache_resp is not None:
                out_arr.append(cache_resp)
            else:

                try:
                    # domain = whois.query(uri)
                    # for domain
                    out_arr.append(self.get_whois(uri))

                    # self.cache.append([uri, str(domain.__dict__)])
                    # out_arr.append(domain.__dict__)
                    
                except Exception as e:
                    print("WHOIS:", e, file=sys.stderr)
        return {'WhoIs': out_arr}
    
    def get_whois(self, uri):
        print(uri)
        data = WebpageResolver.get_html(f"https://www.whois.com/whois/{uri}")
        soup = bs4.BeautifulSoup(data, features="lxml")
        text = soup.find_all("pre")[0].text
        text = re.sub(r'[\n+]', ' ', text).lower()
        text = re.sub(r'\s+', ' ', text).lower()
    
        res = defaultdict(lambda: 'N/A')
        res = {'URL': uri}
        for country in self.tax_havens:
            if country in text:
                res['tax_haven'] = True
        
        for key, reg in self.regexes.items():
            try:
                res[key] = reg.findall(text)[0]
            except IndexError:
                res[key] = 'N/A'

        res['hidden_info'] = any(map(lambda x: 'whoisguard' in str(x).lower(), res.values()))
        res['server_in_poland'] = 'poland' in text.lower()
        print(text)
        return res

if __name__ == "__main__":
    who = WhoIs("atlas")
    data = who.return_data()
    print(data)

