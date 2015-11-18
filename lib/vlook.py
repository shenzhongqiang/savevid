from lxml import etree
from StringIO import StringIO
import re
import requests
import urlparse
import urllib
from lib.site import Site, VideoNotFound

class Vlook(Site):
    def __init__(self):
        pass

    def get_link(self, url):
        r = requests.get(url)
        result = r.text
        patt = re.compile(r'player_src=([^"]*)"')
        match = patt.search(result)
        if not match:
            raise VideoNotFound()

        src = urllib.unquote(match.group(1))
        r = requests.head(src)
        link = r.headers["Location"]
        return link

if __name__ == "__main__":
    site = Vlook()
    print site.get_link('http://www.vlook.cn/show/qs/YklkPTI4OTgwMzc=')

