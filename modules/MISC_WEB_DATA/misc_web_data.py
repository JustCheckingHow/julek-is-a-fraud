from data_source import DataSource
from modules.RGX_GAME.random_page_rgx import RandomRGXExtractor
from modules.WEBPAGE_RESOLVE.webpage_resolver import WebpageResolver
from modules.NUMBER.number import NumberCheck
import csv


class Cache:
    def __init__(self, filename):
        self.filename = filename
        self.delim = '\t'

    def append(self, record):
        with open(f'{self.filename}.tsv', 'a+') as f:
            writer = csv.writer(f, delimiter=self.delim)
            writer.writerow(record)

    def check_cache(self, key):
        try:
            with open(f'{self.filename}.tsv') as f:
                reader = csv.reader(f, delimiter=self.delim)
                for row in reader:
                    if row[0] == key:
                        return row[1]
                return None
        except FileNotFoundError:
            return None


class MiscWebData(DataSource):
    def __init__(self, company_name) -> None:
        super().__init__(company_name)
        self.cache = Cache('modules/MISC_WEB_DATA/cache')

    def return_data(self, **kwargs) -> dict:
        cache_check = self.cache.check_cache(self.company_name)
        if cache_check is not None:
            return {'MiscWebData': cache_check}

        try:
            links = WebpageResolver(self.company_name).return_data()['webpage']
        except IndexError:
            print('MiscWebData error: No webpage found')
            return {'MiscWebData': None}

        data = []
        for link in links:
            try:
                page = WebpageResolver.get_html(
                    link,
                    stash=False,
                    only_cached=False)
                if page is None:
                    continue

                extractor = RandomRGXExtractor()
                extracted = extractor.parse_webpage(page)
                if not extracted:
                    continue

                if len(extracted['phone-polish']) > 0:
                    nc = NumberCheck(self.company_name)
                    matches = []
                    for phone in extracted['phone-polish']:
                        matches += [nc.return_data(number_string=phone)]
                    extracted['phone-polish'] = matches

                data += [dict(extracted)]
            except Exception as e:
                print(e)

        self.cache.append([
            self.company_name, data
        ])

        return {'MiscWebData': data}
