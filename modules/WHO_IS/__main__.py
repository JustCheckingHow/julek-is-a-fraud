from .whois_api import WhoIs

who = WhoIs("comino")
data = who.return_data()
print(data)
