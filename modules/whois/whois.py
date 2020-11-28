from data_source import DataSource
import whois
import signal
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


class WhoIs(DataSource):
    def __init__(self):
        super().__init__(None)
        self.cache = Cache('modules/whois/cache')

    def return_data(self, **kwargs) -> dict:
        uri = kwargs['uri']
        if uri == '':
            raise RuntimeError("Empty URI provided")
        
        cache_resp = self.cache.check_cache(uri)
        if cache_resp is not None:
            print("not None")
            return cache_resp

        signal.signal(signal.SIGALRM, self.signal_handler)
        signal.alarm(30)
        try:
            domain = whois.query(uri)
            self.cache.append([uri, str(domain.__dict__)])
        except:
            print("another one")
            return None

        return domain.__dict__
    
    def signal_handler(self, signum, frame):
        print("handler")
        raise Exception("Timeout")


if __name__ == "__main__":
    #cache = Cache('cache')
    #cache.append(["interia.pl", "aaaa"])

    who = WhoIs()
    data = who.return_data(uri="interia.pl")
    print(data)

