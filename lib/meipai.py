from lxml import etree
from StringIO import StringIO
import requests
from lib.timeit import timeit
from lib.site import Site, VideoNotFound, get_inner_html, get_orig_url

class Meipai(Site):
    def __init__(self):
        pass

    @timeit
    def get_link(self, url):
        r = requests.get(url, timeout=5)
        result = r.text
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(result), parser)
        links = tree.xpath('//div[@id="detailVideo"]/@data-video')
        if len(links) == 0:
            raise VideoNotFound(url)
        vid_link = links[0]

        img_links = tree.xpath('//div[@id="detailVideo"]/img/@src')
        img_link = ''
        if len(img_links) > 0:
            img_link = img_links[0]

        descs = tree.xpath('//h1[@class="detail-description break"]/text()')
        desc = " ".join(descs)
        return {"vid": vid_link, "img": img_link, "desc": desc}

    @timeit
    def search_video(self, keyword, page_num, num_per_page):
        start = (page_num-1) * num_per_page
        url = "http://www.baidu.com/s?q1=%s&q2=&q3=&q4=&lm=0&ft=&q5=&q6=meipai.com&tn=baiduadv&pn=%d&rn=%d" % (keyword, start, num_per_page)
        print url
        r = requests.get(url, timeout=5)
        result = r.text
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(result), parser)
        divs = tree.xpath('//div[@id="content_left"]/div[@id]')
        results = []
        for div in divs:
            a_node = div.find('.//h3/a')
            title = get_inner_html(a_node)
            vid_link = get_orig_url(a_node.get('href'))
            img_node = div.find('.//div/div/a/img')
            img_link = ""
            if img_node is not None:
                img_link = img_node.get('src')
            desc = get_inner_html(div.find('.//div[@class="c-abstract"]'))
            results.append({"title": title,
                "vid": vid_link,
                "img": img_link,
                "desc": desc})
        return results

if __name__ == "__main__":
    meipai = Meipai()
    print meipai.get_link('http://www.meipai.com/media/435782479')
    print meipai.search_video('hello', 1, 2)

