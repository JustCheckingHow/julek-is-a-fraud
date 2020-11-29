from .number import NumberCheck
from modules import WebpageResolver
from modules import RandomRGXExtractor
import time
import csv


# class Cache:
#     def __init__(self, filename):
#         self.filename = filename
#         self.delim = '\t'

#     def append(self, record):
#         with open(f'{self.filename}.tsv', 'a+') as f:
#             writer = csv.writer(f, delimiter=self.delim)
#             writer.writerow(record)

#     def check_cache(self, key):
#         try:
#             with open(f'{self.filename}.tsv') as f:
#                 reader = csv.reader(f, delimiter=self.delim)
#                 for row in reader:
#                     if row[0] == key:
#                         return row[1]
#                 return None
#         except FileNotFoundError:
#             return None


if __name__ == "__main__":
    nc = NumberCheck("testowa1")
    print(nc.return_data(number_string="48221043705"))

    # data = []
    # with open("modules/WEBPAGE_RESOLVE/cache.tsv") as f:
    #    reader = csv.reader(f, delimiter='\t')
    #    for row in reader:
    #        data.append(row[0])

    # print("LEN:", len(data))

    # for el in data:
    #    links = WebpageResolver(el).return_data()['webpage']

    #    for link in links:
    #        try:
    #            page = WebpageResolver.get_html(
    #                link,
    #                stash=False,
    #                only_cached=True)
    #            if page is None:
    #                continue
    #            extractor = RandomRGXExtractor()
    #            extracted = extractor.parse_webpage(page)

    #            if len(extracted['phone-polish']) > 0:
    #                for phone in extracted['phone-polish']:
    #                    nc = NumberCheck(el)
    #                    print(nc.return_data(number_string=phone))
    #                    time.sleep(2)
    #                print(extracted)
    #        except Exception as e:
    #            print(e)
