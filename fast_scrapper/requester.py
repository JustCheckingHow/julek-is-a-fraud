import requests
from multiprocessing import Pool
import pickle

with open("links") as f:
    links = f.read().splitlines()

def f(link):
    r = None
    try:
        r = requests.get(link, timeout=10)
    except:
        return link, None
    return link, r.text
    
with Pool(500) as p:
    out = p.map(f, links[:])

with open("out.pkl", "wb") as f:
    pickle.dump(out, f)
