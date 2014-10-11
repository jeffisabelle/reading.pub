# -*- coding: utf-8 -*-
import urllib2
import pprint
import thumber
import requests

from urlparse import urlparse
from bs4 import BeautifulSoup


class LinkScrapper():
    """
    This module provides a metadata for a given link.
    The metadata contains following information.

    - Meta Tags
    - Possible Thumbnails
    - Image Data
    """

    FULL_URL = ""
    BASE_URL = ""
    DOMAIN = ""
    IMAGE_URLS = []
    TARGET_DATA = ""

    def __init__(self, url):
        if url[0:4] != "http":
            url = "http://" + str(url)

        uri = url.replace("www.", "")
        parsed_uri = urlparse(uri)

        if url.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
            self.TARGET_DATA = ""
        else:
            # headers = {'User-Agent': 'Mozilla/5.0'}
            # r = requests.get(url, headers=headers)
            # self.TARGET_DATA = r.text
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            headers = {'User-Agent': user_agent}
            req = urllib2.Request(url, headers=headers)
            self.TARGET_DATA = urllib2.urlopen(req).read()

        self.FULL_URL = url
        self.DOMAIN = '{uri.netloc}'.format(uri=parsed_uri)
        self.BASE_URL = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        self.IMAGE_URLS = self.get_image_urls(url)

    def get_image_urls(self, url):
        """

        Arguments:
        - `self`:
        - `url`:
        """
        if self.DOMAIN == "facebook.com":
            self.IMG_URLS = ["http://bildir.io/static/img/fb.png"]
            return ["http://bildir.io/static/img/fb.png"]

        if url.endswith('/'):
            url = url[:-1]
        elif url.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            self.IMAGE_URLS = [url]
            return [url]

        soup = BeautifulSoup(self.TARGET_DATA)
        image_tags = soup.find_all('img')
        image_urls = []

        for img in image_tags:
            image_dict = img.attrs
            if "data-src" in image_dict:
                src = image_dict["data-src"]
            elif "src" in image_dict:
                src = image_dict["src"]
            else:
                continue

            if src.startswith('//'):
                image_urls.append("http://" + src[2:])
                continue
            elif src.startswith('http://'):
                image_urls.append(src)
                continue
            elif src.startswith('https://'):
                image_urls.append(src)
                continue
            elif src.startswith('/'):
                image_urls.append(self.BASE_URL + src)
                continue
            elif src.startswith('../'):
                # TODO
                continue

            image_urls.append(url + "/" + src)

        self.IMAGE_URLS = image_urls
        return image_urls

    def get_image_data(self):
        sizes = []
        for image_url in self.IMAGE_URLS:
            if not image_url.endswith(('jpg', 'png', 'gif', 'jpeg')):
                continue
            image_data = thumber.get_sizes(image_url)
            if not image_data[1]:
                continue

            image_size = image_data[0]
            image_width = image_data[1][0]
            image_height = image_data[1][1]
            sizes.append((image_url, image_size, image_width, image_height))

        datas = []
        for size in sizes:
            data = {
                "image_url": size[0],
                "image_size": size[1],
                "image_width": size[2],
                "image_height": size[3]
            }
            datas.append(data)

        return datas

    def get_meta_data(self):
        soup = BeautifulSoup(self.TARGET_DATA)
        meta_tags = soup.find_all('meta')
        m_tags = {}
        for meta in meta_tags:
            if "property" in meta.attrs and "content" in meta.attrs:
                m_tags[meta["property"]] = meta["content"]
            elif "name" in meta.attrs and "content" in meta.attrs:
                m_tags[meta["name"]] = meta["content"]

        return m_tags

    def get_title(self):
        """
        Returns text data of <title> tag.
        """
        meta = self.get_meta_data()
        if "og:title" in meta:
            return meta["og:title"]
        else:
            soup = BeautifulSoup(self.TARGET_DATA)
            title = soup.find('title')
            if title:
                return title.text
            else:
                return "No Title"

    def get_possible_thumbnail(self):
        """
        If the url has opengraph or twitter cards data,
        returns the corresponding image as thumbnail.

        Otherwise, it returns the largest image on the web page.
        """
        meta = self.get_meta_data()
        print meta
        if "og:image" in meta:
            return meta["og:image"]
        elif "twitter:image:src" in meta:
            return meta["twitter:image:src"]
        else:
            images = self.get_image_data()
            temp_url = ""
            temp_width = 0
            for img in images:
                if img["image_width"] > temp_width:
                    temp_url = img["image_url"]
                    temp_width = img["image_width"]

            return temp_url

    def scrape(self):
        scraped = {}
        scraped["domain"] = self.DOMAIN
        scraped["url"] = self.FULL_URL

        # print "--------"
        # print self.get_title()

        scraped["title"] = self.get_title()
        # scraped["images"] = self.get_image_data()
        scraped["meta"] = self.get_meta_data()
        scraped["thumbnail"] = self.get_possible_thumbnail()
        return scraped


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    # tr ş sıkıntı
    # url = "http://www.boxofficeturkiye.com/film/2011446/X-Men:-Gecmis-Gunler-Gelecek.htm"

    # hiç parse etmiyor
    # url = "www.cumhuriyet.com.tr/haber/dunya/79151/350_TL_lik__penis_buyutucu__siparis_etti__15_TL_lik_buyutec_geldi.html"

    # bazı url'lerde og:image full-url olarak verilmemişs
    # örn: og:image: /img/logo.png
    # onlarda domain'le concat et
    url = "https://www.google.com/search?q=%3Cblink%3E"

    ls = LinkScrapper(url)

    scraped = ls.scrape()
    pp.pprint(scraped)
