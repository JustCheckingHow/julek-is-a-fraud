import csv

with open("cache.tsv") as f:
    out = []
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        out.append(row[1])

urls = []
for l in out:
    if l.count(',', 0, len(l)) > 5:
        continue
    urls.extend(l.lower().split(','))

for i in urls:
    print(i)

