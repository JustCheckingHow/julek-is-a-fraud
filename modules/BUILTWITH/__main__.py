from .built_with import BuiltWith
from modules import WebpageResolver
import numpy as np


# WORKING EXAMPLES: Chinatsu and Partners
cache = WebpageResolver('Mango').cache.index
to_search = np.random.choice(cache, size=10)
for i in to_search:
    print(i)
    module = BuiltWith(i)
    print(i, module.return_data())
