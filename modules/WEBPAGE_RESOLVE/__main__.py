from .webpage_resolver import WebpageResolver

test = WebpageResolver("European lnvestment Systems")
res = test.return_data()
print(res)
for i in res:
    print(WebpageResolver.get_html(i)[:5])
