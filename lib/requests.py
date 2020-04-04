# coding=utf-8
# 向服务器发送请求

import OpenSSL
import requests
import urllib3
import logging
import hashlib
import random
import re
import ssl
import socket
from lib.random_header import get_ua

# 全局超时时间
TIMEOUT = 5
# 设置cookie
COOKIE = 'random'


def verify(url):
    if not re.search('http:|https:', url):
        url = 'http://' + url
    return url


class Requests:
    def __init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings()

        self.timeout = TIMEOUT
        self.session = requests.Session()
        self.headers = get_ua()

        if COOKIE == 'random':
            plain = ''.join([random.choice('0123456789') for _ in range(8)])
            md5sum = hashlib.md5()
            md5sum.update(plain.encode('utf-8'))
            md5 = md5sum.hexdigest()
            self.headers.update({'Cookie': 'SESSION=' + md5})
        else:
            self.headers.update(COOKIE)

    def get(self, url):
        url = verify(url)
        try:
            r = self.session.get(url,
                                 timeout=self.timeout,
                                 headers=self.headers,
                                 verify=False,
                                 allow_redirects=False)
            return r
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.Timeout,
                requests.exceptions.SSLError, requests.exceptions.ConnectionError, ssl.SSLError, AttributeError,
                ConnectionRefusedError, socket.timeout, urllib3.exceptions.ReadTimeoutError, OpenSSL.SSL.WantReadError):
            pass
        except Exception as e:
            logging.exception(e)

    def post(self, url, data):
        url = verify(url)
        try:
            r = self.session.post(url,
                                  data=data,
                                  timeout=self.timeout,
                                  headers=self.headers,
                                  verify=False,
                                  allow_redirects=False)
            return r
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.Timeout,
                requests.exceptions.SSLError, requests.exceptions.ConnectionError, ssl.SSLError, AttributeError,
                ConnectionRefusedError, socket.timeout, urllib3.exceptions.ReadTimeoutError, OpenSSL.SSL.WantReadError):
            pass
        except Exception as e:
            logging.exception(e)
