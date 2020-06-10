# -*- coding: UTF-8 -*-
import pymysql


# import json


class MySqlForConfig:
    # 实例化对象
    def __init__(self, config):
        self.db_config = config
        self.conn = None

    # 连接
    def connect(self):
        try:
            config = self.db_config
            self.conn = pymysql.connect(**config)
            cursor = self.conn.cursor()
        except Exception as e:
            print(e.__str__())
            return
        return cursor

    def close(self):
        self.conn.close()

    def query_sql(self, sql):
        cur = self.connect()
        cur.execute(sql)
        self.conn.commit()
        res_list = cur.fetchall()
        cur.close()
        self.conn.close()
        return res_list

    def query_sql_return_dict(self, sql):
        cur = self.connect()
        cur.execute(sql)
        self.conn.commit()
        res_dict = self.dict_fetchall(cur)
        cur.close()
        self.conn.close()
        return res_dict
        # return json.dumps(res_dict, ensure_ascii=False)

    @staticmethod
    def dict_fetchall(cursor):
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    def exec_sql(self, sql):
        cur = self.connect()
        ret = cur.execute(sql)
        self.conn.commit()
        cur.close()
        self.conn.close()
        return ret

    def insert_return_id(self, sql):
        cur = self.connect()
        cur.execute(sql)
        insert_id = int(self.conn.insert_id())  # 最新插入行的主键ID
        self.conn.commit()
        cur.close()
        self.conn.close()
        return insert_id


if __name__ == '__main__':
    usan_db = {'host': '127.0.0.1',
               'user': 'root',
               'password': 'zyj123456',
               'database': 'autotest',
               'port': 3606,
               'charset': "utf8"}
    db = MySqlForConfig(usan_db)
    insert_sql = """select id from TestPlatTestTable where iphone='%s' and flag=1;""" % '12345678911'
    data = db.query_sql(insert_sql)
    print(data[0][0])
