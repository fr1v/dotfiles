#VERSION: 2.03
#AUTHORS: Boris Nagaev (bnagaev@gmail.com), Dan Erusalimchik (danerde@gmail.com)
# This plugin is licensed under the GNU GPL Version 2.

from novaprinter import prettyPrinter
from helpers import retrieve_url
import re
import codecs
try:
    from urllib import quote, unquote
except:
    # python 3
    from urllib.parse import quote, unquote

hit_pattern = re.compile(r'''\s*<a href="(?P<desc_link>.+)">(?P<name>.+)</a>\s*
\s*</td>\s*
\s*<td class="dl">\s*
\s*(?P<size>.+)\s*
\s*</td>\s*
\s*<td class="dl">\s*
\s*<b class="sd">(?P<seeds>.*)</b>\s*
\s*</td>\s*
\s*<td class="dl">\s*
\s*<b class="lc">(?P<leech>.+)</b>\s*''')
tag = re.compile(r'<.*?>')
download = re.compile(r'download.php[^"]*')

class tfile_me(object):
    search_url = 'http://search.tfile.me';
    url = 'http://tfile.me';
    name = 'tfile.me'
    supported_categories = {'all': 0,
                            'movies': 37,
                            'tv': 1068,
                            'music': 67,
                            'games': 98,
                            'anime': 175,
                            'software': 118,
                            'pictures': 1075,
                            'books': 195}
    query_pattern = '%(url)s/?q=%(q)s&c=%(f)i&start=%(start)i&o=newest&to=1&io=1'

    def __init__(self):
        pass

    def to_cp1251(self, text):
        try:
            # Python 2
            return text.decode('utf-8').encode('cp1251')
        except:
            # Python 3
            return codecs.encode(text, 'cp1251')

    def get_link(self, desc_link):
        html = retrieve_url(desc_link)
        for download_url in download.finditer(html):
            return self.url + '/forum/' + download_url.group()

    def search_page(self, what, cat, start):
        what = unquote(what)
        params = {}
        params['url'] = self.search_url
        params['q'] = quote(self.to_cp1251(what))
        params['f'] = self.supported_categories[cat]
        params['start'] = start
        dat = retrieve_url(self.query_pattern % params)
        for hit in hit_pattern.finditer(dat):
            d = hit.groupdict()
            d['link'] = self.get_link(d['desc_link'])
            d['engine_url'] = self.url
            d['name'] = tag.sub('', d['name'])
            if d['link']:
                yield d


    def search(self, what, cat='all'):
        start = 0
        while True:
            ds = list(self.search_page(what, cat, start))
            if not ds:
                break
            for d in ds:
                prettyPrinter(d)
            start += 25

