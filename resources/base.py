# -*-coding:utf-8-*-
import pymysql
#from resource.pool import MysqlPool #使用连接池就去掉注释
#from common.logger import logger

#mysql_pool = MysqlPool() #使用连接池就去掉注释


class BaseDb:
    def __init__(self):
        """
        单例模式的连接池中拿去一个游标，并在使用完成后关闭
        """
        # 使用连接池就去掉注释
        # self.pool = mysql_pool
        # self.conn = self.pool.get_connection()

        self.conn = pymysql.connect(host='39.105.9.20', user='root', password='bigdata_oil', db='cxd_data', charset='utf8')
        # 如果要使用with conn.cursor() as cursor: 的格式写到这里就可以了

        self.cur = self.conn.cursor()
        self.dict_cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        #logger.info('db connected')

    def __del__(self):
        self.cur.close()
        self.dict_cur.close()
        self.conn.close()