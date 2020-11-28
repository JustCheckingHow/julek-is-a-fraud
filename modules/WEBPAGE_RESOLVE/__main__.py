from .webpage_resolver import WebpageResolver

test = WebpageResolver("wtbitcoin")
res = test.return_data()
print(res)
print(WebpageResolver.get_html(res['webpage'][0]))
