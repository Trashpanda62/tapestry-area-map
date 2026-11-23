"""Regenerate the static SEO blocks in index.html from the PLACES array.
Run after editing PLACES:  python -I tools/build-seo.py
Writes a JSON-LD ItemList and a <noscript> place list between marker comments."""
import re, json, html, pathlib
p = pathlib.Path(__file__).resolve().parent.parent / 'index.html'
s = p.read_text(encoding='utf8')
arr = re.search(r"var PLACES = \[(.*?)\n  \];", s, re.S).group(1)
places = []
for m in re.finditer(r"\{n:'((?:[^'\\]|\\.)+)',[^{}]*?cat:'(\w+)'[^{}]*?at:\[([\d.\-]+),\s*([\d.\-]+)\],\s*mins:'([^']*)'[^{}]*?d:'((?:[^'\\]|\\.)+)'\}", arr):
    n, cat, la, lo, mins, d = m.groups()
    places.append(dict(n=n.replace("\\'", "'"), cat=cat, la=float(la), lo=float(lo), mins=mins, d=d.replace("\\'", "'")))
assert len(places) >= 70, len(places)
ld = {
    "@context": "https://schema.org", "@type": "ItemList",
    "name": "Things to do near Tapestry Acres, Monroe, Tennessee",
    "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "item": {
            "@type": "TouristAttraction", "name": x['n'], "description": x['d'],
            "geo": {"@type": "GeoCoordinates", "latitude": x['la'], "longitude": x['lo']}}}
        for i, x in enumerate([q for q in places if q['mins']])]}
ldblock = '<!--SEO-LD-START--><script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace('</', '<\\/') + '</script><!--SEO-LD-END-->'
li = ''.join('<li><b>%s</b> (%s from the farm): %s</li>' % (html.escape(x['n']), html.escape(x['mins']), html.escape(x['d'])) for x in places if x['mins'])
nsblock = '<!--SEO-NS-START--><noscript><h2>Places near Tapestry Acres</h2><ul>' + li + '</ul></noscript><!--SEO-NS-END-->'
def put(s, a, b, blk, anchor):
    pat = re.compile(re.escape(a) + '.*?' + re.escape(b), re.S)
    if pat.search(s):
        return pat.sub(lambda m: blk, s)
    return s.replace(anchor, blk + anchor, 1)
s = put(s, '<!--SEO-LD-START-->', '<!--SEO-LD-END-->', ldblock, '</head>')
s = put(s, '<!--SEO-NS-START-->', '<!--SEO-NS-END-->', nsblock, '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>')
p.write_text(s, encoding='utf8')
print('places', len(places))
