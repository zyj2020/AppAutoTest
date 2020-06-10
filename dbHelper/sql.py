# -*- coding: UTF-8 -*-
import dbHelper.db_conn as db_conn


class MYSQL:
    # 实例化对象
    def __init__(self, host, user, pwd, db, port):
        self.mysql = db_conn.MYSQL(host, user, pwd, db, port)

    # 增删改查
    def query(self, sql):
        result = self.mysql.exec_query(sql)
        return result
