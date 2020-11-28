from .iosco import IOSCOParse

p = IOSCOParse()
cl = p.parse_loop()
df = IOSCOParse.toPandas(cl).to_csv("iosco.tsv", sep='\t')
