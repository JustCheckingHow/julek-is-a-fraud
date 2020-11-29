from data_source import DataSource
from modules import WebpageResolver, TaxHeaven
# import whois
import pythonwhois
import signal
import csv
import sys
import bs4
import re
from collections import defaultdict
from pprint import pprint


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
        super().__init__(None)
        self.tax_havens = TaxHeaven().return_data()['tax_heaven']
        self.cache = Cache('modules/WHO_IS/cache')
        resolv = WebpageResolver(company_name)
        self.company_name = resolv.company_name
        try:
            res = resolv.return_data()['webpage']
            self.webpages = list(set(res))
        except IndexError as e:
            print("WEBPAGE NOT FOUND")
            raise e

    def return_data(self, **kwargs) -> dict:
        out_arr = []
        for uri_with_http in self.webpages:
            uri = uri_with_http.replace('http://', '').replace('https://', '').replace("www.", "")
            if uri[-1] == "/" or uri[-1] == '.':
                uri = uri[:-1]
            # cache_resp = self.cache.check_cache(uri)
            cache_resp = None
            if cache_resp is not None:
                out_arr.append(cache_resp)
            else:

                try:
                    domain = pythonwhois.get_whois(uri)
                    domain['URL'] = uri
                    domain_info_more = self.get_whois(domain)
                    del domain['raw']
                    pprint(domain)
                    domain.update(domain_info_more)
                    
                    res = self.clear_dict(domain)
                    out_arr.append(res)

                except Exception as e:
                    print("WHOIS ERROR:", e, file=sys.stderr)

        result = {'WhoIs': out_arr}
        result['CompanyName'] = self.company_name
        return result
    
    def get_whois(self, response):
        try:
            server = response['whois_server'][0]
            text = pythonwhois.net.get_whois_raw(response['URL'], server)[0]
        except KeyError:
            text = response['raw'][0]
        print(text)
    
        res = defaultdict(lambda: 'N/A')
        res['tax_haven'] = False
        for country in self.tax_havens:
            if country.lower() in text.lower():
                res['tax_haven'] = country

        res['hidden_info'] = any(map(lambda x: 'whoisguard' in str(x).lower() or 'redacted' in str(x).lower(), text))
        res['server_in_poland'] = ('poland' in text.lower() or '.pl' in response['URL'].lower())
        return res

    def clear_dict(self, data):
        res = {}
        res['URL'] = data['URL']
        res['tax_haven'] = data['tax_haven']
        res['hidden_info'] = data['hidden_info']
        res['server_in_poland'] = data['server_in_poland']
        try:
            res['creation_date'] = data['creation_date']
        except KeyError:
            pass
        return res

if __name__ == "__main__":
    who = WhoIs("atlas")
    data = who.return_data()
    print(data)
