from .whois_api import WhoIs

who = WhoIs("European lnvestment Systems")
data = who.return_data()
print(data)
