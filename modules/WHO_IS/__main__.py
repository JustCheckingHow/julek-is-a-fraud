from .whois_api import WhoIs

who = WhoIs("saxo")
data = who.return_data()
print(data)
