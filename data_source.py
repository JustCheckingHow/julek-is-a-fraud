class DataSource:
    """
    Basic class for source of information about a company
    """
    def __init__(self, company_name):
        self.company_name = company_name

    def return_data(self, **kwargs) -> dict:
        """
        Return information about the company
        """
        return None
