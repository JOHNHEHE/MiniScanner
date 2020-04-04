# coding = utf-8
# 数据库操作

import sqlite3
import time
import re
import logging


class Sqldb:
    def __init__(self, dbname):
        self.name = dbname
        self.conn = sqlite3.connect(self.name + '.db', check_same_thread=False)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def create_ports(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time varchar(255),
                ipaddr varchar(255),
                service varchar(255) DEFAULT '',
                port varchar(255) DEFAULT '',
                banner varchar(255) DEFAULT ''
                )
                """)
        except Exception as e:
            pass

    def create_active(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS active (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time varchar(255),
                ipaddr varchar(64),
                state varchar(16)
                )
                """)
        except Exception as e:
            pass

    def create_os(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS os (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time varchar(255),
                ipaddr varchar(64),
                os varchar(1024) DEFAULT ''
                )
                """)
        except Exception as e:
            pass

    def create_crawl(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS crawl (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time varchar(255),
                domain varchar(255),
                content varchar(1024) DEFAULT ''
                )
                """)
        except Exception as e:
            logging.exception(e)

    def insert(self, query, values):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, values)
        except Exception as e:
            logging.exception(e)

    def set_ports(self, ipaddr, result):
        self.create_ports()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for i in result:
            service = i.get('server')
            port = i.get('port')
            banner = i.get('banner')
            banner = re.sub('<', '', banner)
            banner = re.sub('>', '', banner)
            values = (timestamp, ipaddr, service, port, banner)
            query = "INSERT OR IGNORE INTO ports (time, ipaddr, service, port, banner) VALUES (?,?,?,?,?)"
            self.insert(query, values)
        self.commit()
        self.close()

    def set_active(self, ipaddr, state):
        self.create_active()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        values = (timestamp, ipaddr, state)
        query = "INSERT OR IGNORE INTO active (time, ipaddr, state) VALUES (?,?,?)"
        self.insert(query, values)
        self.commit()
        self.close()

    def set_os(self, ipaddr, os):
        self.create_os()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        values = (timestamp, ipaddr, os)
        query = "INSERT OR IGNORE INTO os (time, ipaddr, os) VALUES (?,?,?)"
        self.insert(query, values)
        self.commit()
        self.close()

    def set_crawl(self, domain, result):
        self.create_crawl()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for i in result:
            values = (timestamp, domain, i)
            query = "INSERT OR IGNORE INTO crawl (time, domain, content) VALUES (?,?,?)"
            self.insert(query, values)
        self.commit()
        self.close()

    def query(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            values = cursor.fetchall()
            return values
        except sqlite3.OperationalError:
            pass
        except Exception as e:
            logging.exception(e)
        finally:
            self.commit()
            self.close()
