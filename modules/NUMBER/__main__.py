from .number import NumberCheck
from modules import WebpageResolver
from modules import RandomRGXExtractor
import time
import csv

if __name__ == "__main__":
    nc = NumberCheck("testowa1")
    print(nc.return_data(number_string="48221043705"))

    #data = []
    #with open("modules/WEBPAGE_RESOLVE/cache.tsv") as f:
    #    reader = csv.reader(f, delimiter='\t')
    #    for row in reader:
    #        data.append(row[0])

    #print("LEN:", len(data))

    #for el in data[:]:
    #    links = WebpageResolver(el).return_data()['webpage']
    #    
    #    for link in links:
    #        try:
    #            page = WebpageResolver.get_html(link, False, True)
    #            if page is None:
    #                continue
    #            extractor = RandomRGXExtractor()
    #            extracted = extractor.parse_webpage(page)
    #            
    #            if len(extracted['phone-polish']) > 0:
    #                for phone in extracted['phone-polish']:
    #                    nc = NumberCheck(el)
    #                    print(nc.return_data(number_string=phone))
    #                    time.sleep(2)
    #                print(extracted)
    #        except Exception as e:
    #            print(e)
    #            pass

