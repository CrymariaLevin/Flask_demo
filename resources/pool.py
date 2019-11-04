# -*- coding:utf-8 -*-
"""
数据库连接池
"""
from DBUtils.PooledDB import PooledDB
import pymysql
# from settings import MySQL_USER, MySQL_PORT, MySQL_HOST, MySQL_DB_NAME, MySQL_PASSWD


class MysqlPool:
    def __init__(self, charset="utf8", mincached=1, maxcached=2, maxconnections=100, blocking=True, maxshared=0):
        """
         生成MySQL数据库连接池
        :param charset: 使用字符集
        :param mincached: 最少的空闲连接数，如果空闲连接数小于这个数，pool会创建一个新的连接
        :param maxcached: 最大的空闲连接数，如果空闲连接数大于这个数，pool会关闭空闲连接
        :param maxconnections: 最大的连接数
        :param blocking: 当连接数达到最大的连接数时，在请求连接的时候，如果这个值是True，请求连接的程序会一直等待，
                         直到当前连接数小于最大连接数，如果这个值是False，会报错，
        :param maxshared: 当连接数达到这个数，新请求的连接会分享已经分配出去的连接
        """
        db_config = {
            "host": '39.105.9.20',
            "port": 3306,
            "user": 'root',
            "passwd": 'bigdata_oil',
            "db": 'cxd_data',
            "charset": 'utf8'
        }
        self.pool = PooledDB(pymysql, mincached=mincached, maxcached=maxcached,maxconnections=maxconnections,
                             blocking=blocking,maxshared=maxshared, **db_config)

    def get_connection(self):
        return self.pool.connection()

    def close(self):
        self.pool.close()

    def __del__(self):
        self.close()


# 获取mysql数据库服务器的连接
def get_dbservice_mysql_conn():
    """
    :return: Object  MySQL Connection
    """
    global common_pool

    if not common_pool or not isinstance(common_pool, MysqlPool):
        common_pool = MysqlPool()
    return common_pool.get_connection()