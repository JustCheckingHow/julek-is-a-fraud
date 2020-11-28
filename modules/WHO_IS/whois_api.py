from data_source import DataSource
from modules import WebpageResolver
import whois
import signal
import csv
import sys

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
            uri = uri_with_http.replace('http://', '')
            cache_resp = self.cache.check_cache(uri)
            if cache_resp is not None:
                out_arr.append(cache_resp)
            else:

            #signal.signal(signal.SIGALRM, self.signal_handler)
            #signal.alarm(30)
                try:
                    domain = whois.query(uri)
                    self.cache.append([uri, str(domain.__dict__)])
                    out_arr.append(domain.__dict__)
                except Exception as e:
                    print("WHOIS:", e, file=sys.stderr)
            
        return {'WhoIs': out_arr}
    
    #def signal_handler(self, signum, frame):
    #    print("handler")
    #    raise Exception("Timeout")


if __name__ == "__main__":
    who = WhoIs("aviva")
    data = who.return_data()
    print(data)

