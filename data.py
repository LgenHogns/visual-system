# coding=utf-8

import pymysql
import configparser
from dbutils.persistent_db import PersistentDB


class DBData:
    def __init__(self):
        cnf = configparser.ConfigParser()
        cnf.read('settings.ini')

        self.pool = PersistentDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表
            ping=0,  # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            closeable=False,  # 如果为False时， conn.close() 实际上被忽略，供下次使用，再线程关闭时，才会自动关闭链接。如果为True时， conn.close()则关闭链接，那么再次调用pool.connection时就会报错，因为已经真的关闭了连接
            threadlocal=None,  # 本线程独享值得对象，用于保存链接对象，如果链接对象被重置
            host=cnf.get('mysql', 'db_ip'),
            port=int(cnf.get('mysql', 'db_port')),
            user=cnf.get('mysql', 'db_user'),
            passwd=cnf.get('mysql', 'db_password'),
            db=cnf.get('mysql', 'db_database')
        )
        
        db = self.pool.connection(shareable=False)
        cursor = db.cursor()

        cursor.execute('''
            create table if not exists now_tid(
                num int
            )
        ''')

        cursor.execute('''
            create table if not exists cardinality(
                tid int,
                num int
            )
        ''')

        cursor.execute('''
            create table if not exists entropy(
                tid int,
                num double
            )
        ''')

        cursor.execute('''
            create table if not exists heavy_hitter(
                tid int,
                src_ip int unsigned,
                dst_ip int unsigned,
                src_port smallint unsigned,
                dst_port int unsigned,
                protocol int,
                size int unsigned
            )
        ''')

        cursor.execute('''
            create table if not exists heavy_change(
                tid int,
                src_ip int unsigned,
                dst_ip int unsigned,
                src_port smallint unsigned,
                dst_port int unsigned,
                protocol int,
                increment int
            )
        ''')

        cursor.execute('''
            create table if not exists flows(
                tid int,
                src_ip int unsigned,
                dst_ip int unsigned,
                src_port smallint unsigned,
                dst_port int unsigned,
                protocol int,
                size int
            )
        ''')

        cursor.execute('''
            create table if not exists latency(
                tid int,
                src_ip int unsigned,
                dst_ip int unsigned,
                src_port smallint unsigned,
                dst_port int unsigned,
                protocol int,
                switch_id int
            )
        ''')

        cursor.execute('''
            create table if not exists distribution(
                tid int,
                idx int,
                num double
            )
        ''')

        db.commit()
        cursor.close()
        db.close()

    def set_tid(self, tid):
        db = self.pool.connection(shareable=False)
        cursor = db.cursor()

        query = 'insert into now_tid values (%s)'
        cursor.execute(query, tid)

        db.commit()
        cursor.close()
        db.close()

    def get_tid(self):
        db = self.pool.connection(shareable=False)
        cursor = db.cursor()

        query = 'select max(num) from now_tid'
        cursor.execute(query)
        result = cursor.fetchall()

        db.commit()
        cursor.close()
        db.close()

        return result

    def set_heavy_hitter(self, tid, value):
        db = self.pool.connection(shareable=False)
        cursor = db.cursor()

        query = 'insert into heavy_hitter values (' + \
            str(tid)+',%s,%s,%s,%s,%s,%s)'
        cursor.executemany(query, value)

        db.commit()
        cursor.close()
        db.close()

    def get_heavy_hitter(self):
        db = self.pool.connection(shareable=False)
        cursor = db.cursor()

        query = 'select * from heavy_hitter order by size desc limit 2000'
        cursor.execute(query)
        result = cursor.fetchall()

        db.commit()
        cursor.close()
        db.close()

        return result

    def set_heavy_change(self, tid, value):
        db = self.pool.connection(shareable=False)
        cursor = db.cursor()

        query = 'insert into heavy_change values (' + \
            str(tid)+',%s,%s,%s,%s,%s,%s)'
        cursor.executemany(query, value)

        db.commit()
        cursor.close()
        db.close()

    def get_heavy_change(self):
        db = self.pool.connection(shareable=False)
        cursor = db.cursor()

        query = 'select * from heavy_change order by increment desc limit 2000'
        cursor.execute(query)
        result = cursor.fetchall()

        db.commit()
        cursor.close()
        db.close()

        return result

    def set_switch(self, tid, value):
        db = self.pool.connection(shareable=False)
        cursor = db.cursor()

        query = 'insert into latency values ('+str(tid)+',%s,%s,%s,%s,%s,%s)'
        cursor.executemany(query, value)

        db.commit()
        cursor.close()
        db.close()

    def get_switch(self):
        db = self.pool.connection(shareable=False)
        cursor = db.cursor()

        query = 'select * from latency limit 200'
        cursor.execute(query)
        result = cursor.fetchall()

        db.commit()
        cursor.close()
        db.close()

        return result

    def set_distri(self, tid, value):
        db = self.pool.connection(shareable=False)
        cursor = db.cursor()

        query = 'insert into distribution values ('+str(tid)+',%s,%s)'
        cursor.executemany(query, value)

        db.commit()
        cursor.close()
        db.close()

    def get_distri(self):
        db = self.pool.connection(shareable=False)
        cursor = db.cursor()

        query = 'select * from distribution order by idx'
        cursor.execute(query)
        result = cursor.fetchall()

        db.commit()
        cursor.close()
        db.close()
        return result

    def set_size(self, tid, value):
        db = self.pool.connection(shareable=False)
        cursor = db.cursor()

        query = 'insert into flows values ('+str(tid)+',%s,%s,%s,%s,%s,%s)'
        cursor.executemany(query, value)

        db.commit()
        cursor.close()
        db.close()

    def get_size(self):
        db = self.pool.connection(shareable=False)
        cursor = db.cursor()

        query = 'select * from flows limit 200'
        cursor.execute(query)
        result = cursor.fetchall()

        db.commit()
        cursor.close()
        db.close()

        return result

    def set_cardinality(self, tid, value):
        db = self.pool.connection(shareable=False)
        cursor = db.cursor()

        query = 'insert into cardinality values ('+str(tid)+',%s)'
        cursor.execute(query, (value))

        db.commit()
        cursor.close()
        db.close()

    def get_cardinality(self):
        db = self.pool.connection(shareable=False)
        cursor = db.cursor()

        query = 'select * from cardinality'
        cursor.execute(query)
        result = cursor.fetchall()

        db.commit()
        cursor.close()
        db.close()

        return result

    def set_entropy(self, tid, value):
        db = self.pool.connection(shareable=False)
        cursor = db.cursor()

        query = 'insert into entropy values ('+str(tid)+',%s)'
        cursor.execute(query, (value))

        db.commit()
        cursor.close()
        db.close()

    def get_entropy(self):
        db = self.pool.connection(shareable=False)
        cursor = db.cursor()

        query = 'select * from entropy'
        cursor.execute(query)
        result = cursor.fetchall()

        db.commit()
        cursor.close()
        db.close()

        return result
