import pymysql


class MysqlDB(object):
    '''连接数据库'''
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            port='3306',
            user='root',
            password='mysql',
            database='???',
            charset='uft8'
        )
        self.cursor = self.conn.cursor()

    def get(self):
        sql = "SELECT * FROM card;"
        row_count = self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return row_count, data

    def close(self):
        return self.cursor.close()


if __name__ == '__main__':
    sq = MysqlDB()
    sq.get()
    sq.close()