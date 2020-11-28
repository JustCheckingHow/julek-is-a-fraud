from .webpage_resolver import WebpageResolver

test = WebpageResolver("aviva")
res = test.return_data()
print(WebpageResolver.get_links_from_page(res['webpage'][0]))
