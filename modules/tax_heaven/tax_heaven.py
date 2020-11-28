from data_source import DataSource

class TaxHeaven(DataSource):
    def __init__(self):
        super().__init__(None)
        self.data_location = "modules/tax_heaven/data.tsv"

    def return_data(self, **kwargs) -> dict:
        with open(self.data_location) as f:
            data = f.read().splitlines()
        out_dict = {}
        out_dict['tax_heaven'] = data
        return out_dict

if __name__ == "__main__":
    th = TaxHeaven()
    data = th.return_data(data=None)
    print(data)

