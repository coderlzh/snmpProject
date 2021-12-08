# connect_db：连接数据库，并操作数据库
import pymysql

class OperationMysql:

    def __init__(self):
        # 创建一个连接数据库的对象
        self.conn = pymysql.connect(
            host='127.0.0.1',  # 连接的数据库服务器主机名
            port=3306,  # 数据库端口号
            user='root',  # 数据库登录用户名
            passwd='root',
            db='test',  # 数据库名称
            charset='utf8',  # 连接编码
            cursorclass=pymysql.cursors.DictCursor
        )
        # 使用cursor()方法创建一个游标对象，用于操作数据库
        self.cur = self.conn.cursor()

    # 查询一条数据
    def search_one(self, sql):
        self.cur.execute(sql)
        result = self.cur.fetchone()  # 显示所有结果
        return result

    # 查询多条数据
    def search_all(self, sql):
        self.cur.execute(sql)
        result = self.cur.fetchall()  # 显示所有结果
        return result

    # 更新SQL
    def updata_one(self, sql):
        try:
            self.cur.execute(sql)  # 执行sql
            self.conn.commit()  # 增删改操作完数据库后，需要执行提交操作
        except Exception as e:
            # 发生错误时回滚
            print(e)
            self.conn.rollback()
        self.conn.close()  # 记得关闭数据库连接

    def updata_all(self, sql, data):
        try:
            self.cur.executemany(sql,data)  # 执行sql
            self.conn.commit()  # 增删改操作完数据库后，需要执行提交操作
        except Exception as e:
            # 发生错误时回滚
            print(e)
            self.conn.rollback()
        self.conn.close()  # 记得关闭数据库连接


    # 插入SQL
    def insert_one(self, sql):
        try:
            self.cur.execute(sql)  # 执行sql
            self.conn.commit()  # 增删改操作完数据库后，需要执行提交操作
            self.conn.close()
        except Exception as e:
            # 发生错误时回滚
            self.conn.rollback()
            self.conn.close()
            return 'Error:%s' % (e)

    # 插入SQL
    def insert_all(self, sql,data):
        try:
            self.cur.executemany(sql,data)  # 执行sql
            self.conn.commit()  # 增删改操作完数据库后，需要执行提交操作
            self.conn.close()
        except Exception as e:
            # 发生错误时回滚
            self.conn.rollback()
            self.conn.close()
            return 'Error:%s' % (e)

    # 删除SQL
    def delete_one(self, sql):
        try:
            self.cur.execute(sql)  # 执行sql
            self.conn.commit()  # 增删改操作完数据库后，需要执行提交操作
        except:
            # 发生错误时回滚
            self.conn.rollback()
        self.conn.close()

    def create_one(self, sql):
        try:
            self.cur.execute(sql)  # 执行sql
            self.conn.commit()  # 增删改操作完数据库后，需要执行提交操作
            self.conn.close()
        except Exception as e:
            # 发生错误时回滚
            self.conn.rollback()
            self.conn.close()
            return 'Error:%s. Create table failed because %s'%(e.args[0],e.args[1])

    def drop_one(self, sql):
        try:
            self.cur.execute(sql)  # 执行sql
            self.conn.commit()  # 增删改操作完数据库后，需要执行提交操作
            self.conn.close()
        except Exception as e:
            # 发生错误时回滚
            self.conn.rollback()
            self.conn.close()
            return 'Error:%s. Drop table failed because %s' % (e.args[0], e.args[1])

if __name__ == '__main__':
    op_mysql = OperationMysql()