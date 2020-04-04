# coding=utf-8
# 操作系统检测

import time
import nmap
import logging
import xml
from lib.output import console

# 数据存储
from lib.sql import Sqldb


def save(dbname, ipaddr, os):
    Sqldb(dbname).set_os(ipaddr, os)


def osdetect(ip, dbname):
    nm = nmap.PortScanner()
    try:
        result = nm.scan(hosts=ip, arguments='-O')
        for k, v in result.get('scan').items():
            if v.get('osmatch'):
                for i in v.get('osmatch'):
                    # 从namp给出的报告中提取检测系统的名称以及对应正确率
                    console('OsScan', ip, i.get('name') + ' accuracy:' + i.get('accuracy') + '\n')
                    save(dbname, ip, i.get('name') + ' accuracy:' + i.get('accuracy'))
            else:
                break
    except (xml.etree.ElementTree.ParseError, nmap.nmap.PortScannerError):
        pass
    except Exception as e:
        console('OsScan', ip, 'None\n')
        logging.exception(e)


if __name__ == "__main__":
    start_time = time.time()
    osdetect('172.19.249.117', 'os_result')
    end_time = time.time()
    print('\nrunning {0:.3f} seconds'.format(end_time - start_time))
    # print(Sqldb('os_result').query('select * from os'))

