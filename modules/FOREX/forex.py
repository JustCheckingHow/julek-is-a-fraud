from data_source import DataSource
import json

STATIC_FILE = 'modules/FOREX/all_companies.json'

DATA = json.load(open(STATIC_FILE, 'r'))


class ForexReview(DataSource):
    def __init__(self, company_name) -> None:
        super().__init__(company_name)

    def return_data(self, **kwargs) -> dict:
        for el in DATA:
            if self.company_name in el['org'] or self.company_name in el[
                    'company']:
                return {'FOREX': el}

        return {'FOREX': ''}