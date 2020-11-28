from .webpage_resolver import WebpageResolver

test = WebpageResolver("chuj")
res = test.return_data()
print(res)
# print(WebpageResolver.get_links_from_page(res['webpage'][0]))
