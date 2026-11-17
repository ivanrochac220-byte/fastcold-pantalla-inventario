import sys, base64
html, neg, col = sys.argv[1:4]
uri = lambda p: 'data:image/png;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
t = open(html, encoding='utf-8').read()
assert '__LOGO_NEG__' in t and '__LOGO_COLOR__' in t
t = t.replace('__LOGO_NEG__', uri(neg)).replace('__LOGO_COLOR__', uri(col))
open(html, 'w', encoding='utf-8').write(t); print(len(t)//1024, 'KB')
