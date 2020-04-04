# coding=utf-8
# 主机存活扫描

import concurrent.futures
import subprocess
import re
import sys
import time
import dns.resolver
import logging
from urllib import parse
from lib.output import console
from lib.sql import Sqldb


class ActiveCheck:
    def __init__(self, hosts, dbname):
        self.hosts = hosts
        self.out = []
        self.dbname = dbname

    # 数据存储
    def save(self, ipaddr, state):
        Sqldb(self.dbname).set_active(ipaddr, state)

    def check(self, url):
        loc = parse.urlparse(url)
        if getattr(loc, 'netloc'):
            host = loc.netloc
        else:
            host = loc.path

        try:
            # 判断是IP还是域名，如果是域名的话进行域名解析
            if not re.search(r'\d+\.\d+\.\d+\.\d+', host):
                # 验证DNS存活并且不能解析特殊的DNS
                resolver = dns.resolver.Resolver()
                a = resolver.query(host, 'A')
                for i in a.response.answer:
                    for j in i.items:
                        if hasattr(j, 'address'):
                            if re.search(r'1\.1\.1\.1|8\.8\.8\.8|127\.0\.0\.1|114\.114\.114\.114|0\.0\.0\.0', j.address):
                                return False
            try:
                # 指定Echo数据包数为2，指定超时间隔为1ms
                subprocess.check_output(['ping', '-n', '2', '-w', '1', host])
                console('PING', host, "is alive\n")
                self.save(host, 'alive')
                self.out.append(url)
            except (AttributeError, subprocess.CalledProcessError):
                console('PING', host, "is not alive\n")
                self.save(host, 'not alive')
                return False
            except Exception as e:
                logging.exception(e)
                return False

        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
            console('DnsCheck', host, "No A record\n")
            self.save(host, 'No A record')
        except dns.exception.Timeout:
            console('DnsCheck', host, "Timeout\n")
            self.save(host, 'Timeout')
        except Exception as e:
            logging.exception(e)
            return False

    def disable(self):
        # 禁止扫描敏感域名
        for i in self.out:
            if re.search(r'gov\.cn|edu\.cn|\.mil|\.aero|\.int|\.go\.\w+$|\.ac\.\w+$', i):
                console('Disable', i, "Please do not scan this domain\n\n")
                sys.exit(1)

    def pool(self):
        try:
            # 使用线程池，线程数最大为20
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                result = {executor.submit(self.check, i): i for i in self.hosts}
                for future in concurrent.futures.as_completed(result, timeout=3):
                    future.result()
        except (EOFError, concurrent.futures._base.TimeoutError):
            pass
        except Exception as e:
            logging.exception(e)
        self.disable()
        return self.out


if __name__ == "__main__":
    start_time = time.time()
    active_hosts = ActiveCheck(['https://www.baidu.com'], 'active_result').pool()
    end_time = time.time()
    print('\nrunning {0:.3f} seconds'.format(end_time - start_time))
    # print(Sqldb('active_result').query('select * from active'))
