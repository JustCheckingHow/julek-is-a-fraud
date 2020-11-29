from modules.WEBPAGE_RESOLVE.webpage_resolver import DATA
from data_source import DataSource
from modules import WebpageResolver
from collections import defaultdict


class Network(DataSource):
    def __init__(self, company_name):
        super().__init__(company_name)
        resolv = WebpageResolver(company_name)
        self.company_name = resolv.company_name
        self.data_sources = {"Webpages": resolv.cache}

    def return_data(self, **kwargs):
        res = defaultdict(list)
        webpage_ref = self.data_sources['Webpages'].loc[self.company_name].values[0].split(",")
        if ',' in self.company_name and len(webpage_ref)>=3:
            webpage_ref = webpage_ref[:-3]

        for page in webpage_ref:
            filt = self.data_sources['Webpages']['rank'].apply(lambda x: page in x)
            present = self.data_sources['Webpages'][filt]
            for company in present.index:
                if company != self.company_name:
                    res['Webpages'].append(company)

        # Protect against a random crap from supervisors' pages
        if len(res['Webpages'])>10:
            res['Webpages'] = []

        return {"ConnectionsNetwork": dict(res)}

    def find_company(self, name):
        names = self.data_sources['Webpages'].index
        matching = filter(lambda x: name.lower() in x.lower(), names)
        return {"matching": list(matching)}
    # @staticmethod
    # def get_companies_for_url(url):
    #     filtered = DATA['rank'].apply(lambda x: url in x)