from data_source import DataSource
from modules.RGX_GAME.random_page_rgx import RandomRGXExtractor
from modules.WEBPAGE_RESOLVE.webpage_resolver import WebpageResolver
from modules.NUMBER.number import NumberCheck


class MiscWebData(DataSource):
    def __init__(self, company_name) -> None:
        super().__init__(company_name)

    def return_data(self, **kwargs) -> dict:
        try:
            links = WebpageResolver(self.company_name).return_data()['webpage']
        except IndexError:
            print('MiscWebData error: No webpage found')
            return {'MiscWebData': None}

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

                print(extracted)
                # if len(extracted['phone-polish']) > 0:
                #     for phone in extracted['phone-polish']:
                #         nc = NumberCheck(el)
                #         print(nc.return_data(number_string=phone))
                #         time.sleep(2)
                #     print(extracted)
            except Exception as e:
                print(e)

        data = None
        return {'MiscWebData': data}
