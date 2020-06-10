import pymssql


class SqlServer:
    def __init__(self, config):
        self.db_config = config
        self.conn = None

    def conn_db(self):
        try:
            config = self.db_config
            self.conn = pymssql.connect(**config)
            cursor = self.conn.cursor()
        except Exception as e:
            print(e.__str__())
            return
        return cursor

    def insert(self, sql):
        try:
            cursor = self.conn_db()
            cursor.execute(sql)
            self.conn.commit()
            # cursor.fetchall()
        except Exception as ex:
            self.conn.rollback()
            raise ex
        finally:
            self.conn.close()

    def insert_return_id(self, sql):
        insert_id = 0
        try:
            cursor = self.conn_db()
            cursor.execute(sql)
            self.conn.commit()
            insert_id = cursor.lastrowid
        except Exception as ex:
            self.conn.rollback()
            raise ex
        finally:
            self.conn.close()
            return insert_id

    def query(self, sql):
        cursor = self.conn_db()
        cursor.execute(sql)
        data = cursor.fetchall()
        self.conn.close()
        return data

    def update(self, sql):
        cursor = self.conn_db()
        cursor.execute(sql)
        self.conn.commit()
        # cursor.fetchall()
        self.conn.close()
