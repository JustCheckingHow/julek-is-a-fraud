from data_source import DataSource
from modules import WebpageResolver
import builtwith
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

class BuiltWith(DataSource):
    def __init__(self, company_name):
        super().__init__(company_name)
        self.cache = Cache("modules/BUILTWITH/cache")
        self.resolv = WebpageResolver(company_name)

    def return_data(self):
        temp_cache = self.cache.check_cache(self.company_name)
        if temp_cache is not None:
            return {"BuiltWith": temp_cache}

        out = []
        for link in self.resolv.return_data()['webpage']:
            try:
                out.append(builtwith.builtwith(link))
            except Exception as e:
                print(e, "i co z tego")

        self.cache.append([self.company_name, out])
        return {"BuiltWith": out}

            
if __name__ == "__main__":
    bw = BuiltWith("COOPER MARKETS s.r.o")
    print(bw.return_data())
        

