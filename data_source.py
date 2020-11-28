class DataSource:
    """
    Basic class for source of information about a company
    """
    def __init__(self, companyName):
        self.companyName = companyName

    def return_data(self, **kwargs) -> dict:
        """
        Return information about the company
        """
        return None
