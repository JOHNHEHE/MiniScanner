# coding=utf-8
# 爬取网页

import concurrent.futures
import re
import logging
import time
from lib.output import console
from lxml import etree
from lib.requests import Requests
from urllib import parse
from lib.sql import Sqldb


def de_url(urls):
    # 分解url地址
    urls = list(set(urls))
    result = []
    okurl = []
    for i in urls:
        urlparse = parse.urlparse(i)
        path = urlparse.path
        if path and path.split('/')[-2]:
            key = path.split('/')[-2]
            if key not in result:
                result.append(key)
                okurl.append(i)
        else:
            okurl.append(i)
    return okurl


class Crawl:
    def __init__(self, host, dbname):
        self.urls = []
        self.domain = ''
        self.dbname = dbname
        self.host = host
        self.result = []
        self.req = Requests()

    # 数据存储
    def save(self, domain, result):
        Sqldb(self.dbname).set_crawl(domain, result)

    def extr(self, url, body):
        # html页面内爬取邮箱
        email = re.findall(r'\b[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)+', body)
        if email:
            self.result.extend(list(map(lambda x: 'URL: ' + url + '  Email: ' + x, email)))
        # html页面内爬取手机号
        phone = re.findall(
            r'\b(?:133|149|153|173|177|180|181|189|199|135|136|137|138|139|147|150|151|198|130|131|132|155|156|171|175|176|185|186|166)[0-9]{8}\b',
            body)
        if phone:
            self.result.extend(list(map(lambda x: 'URL: ' + url + '  Phone: ' + x, phone)))
        # html注释内爬取ip地址
        ipaddr = re.findall(
            r'(?<=<!--).*((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)).*(?=-->)',
            body)
        if ipaddr:
            self.result.extend(list(map(lambda x: 'IP: ' + x, ipaddr)))
        # html注释内爬取https连接
        links = re.findall(r'(?<=<!--).{0,120}((?:http|https):[\w\./\?\-=&]+).{0,120}(?=-->)', body)
        if links:
            self.result.extend(list(map(lambda x: 'URL: ' + url + '  Links: ' + x, links)))
        # html注释内爬取a连接
        links2 = re.findall(r'(?<=<!--).{0,120}a\shref="([\-\w\.\?:=\&/]+)".{0,120}(?=-->)', body)
        if links2:
            self.result.extend(list(map(lambda x: 'URL: ' + url + '  Links: ' + x, links2)))

    def parse_html(self, host):
        # 爬取网页
        try:
            r = self.req.get(host)  # 获取服务器响应报文
            self.extr(r.url, r.text)
            urlparse = parse.urlparse(host)
            domain = urlparse.netloc
            if not self.domain:
                self.domain = domain
            html = etree.HTML(r.text)
            result = html.xpath('//a/@href')    # 将爬取的链接添加到结果中
            # 给从html解析出的链接元素加上协议头
            for link in result:
                if not re.search('#|mail*|^/$|javascript', link):
                    if 'http' not in link:
                        if urlparse.netloc:
                            link = urlparse.scheme + '://' + urlparse.netloc + '/' + link
                        else:
                            link = 'http://' + host + '/' + link
                    if domain in link:
                        if '=' not in link:
                            self.urls.append(link)
        except (UnboundLocalError, AttributeError, ValueError):
            pass
        except Exception as e:
            logging.exception(e)
            
        self.urls = de_url(self.urls)
        return list(set(self.urls))

    def pool(self):
        result = self.parse_html(self.host)
        try:
            # 使用线程池，线程数最大为30，对页面内跳转链接进行爬取
            with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
                futures = [executor.submit(self.parse_html, i) for i in result]
                for future in concurrent.futures.as_completed(futures, timeout=3):
                    future.result()
        except (EOFError, concurrent.futures._base.TimeoutError):
            pass
        except Exception as e:
            logging.exception(e)

        self.result = list(set(self.result))

        for i in self.result:
            console('Crawl', self.host, i + '\n')

        self.save(self.domain, self.result)


if __name__ == "__main__":
    start_time = time.time()
    Crawl('www.sohu.com', 'crawl_result').pool()
    end_time = time.time()
    print('\nrunning {0:.3f} seconds'.format(end_time - start_time))
    # print(Sqldb('crawl_result').query('select * from crawl'))
