from .whois_api import WhoIs

who = WhoIs("10CryptoMarket")
data = who.return_data()
print(data)
