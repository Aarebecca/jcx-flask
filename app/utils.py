import math
import pymysql
from app.config import ProductionConfig as Pr


def custom_paginator(current_page, num_page, max_page):
    middle = math.ceil(max_page/2)
    if num_page <= max_page:
        start = 1
        end = num_page
    elif current_page <= middle:
        start = 1
        end = max_page
    elif middle < current_page < num_page - middle+1:
        start = current_page - middle
        end = current_page + middle - 1
    else:
        start = num_page - max_page + 1
        end = num_page
    return start, end


class SQL:
    db = None

    def __init__(self):
        # 读入配置文件
        self.db = pymysql.connect(host=Pr.SQL_HOST, user=Pr.SQL_USER, password=Pr.SQL_PSW, database=Pr.SQL_DB,
                                  port=Pr.SQL_PORT)

    # select查询，并将结果格式话为字典
    def query(self, sql):
        cur = self.db.cursor()
        try:
            cur.execute(sql)
            print(sql)
            cur_des = cur.description
            results = cur.fetchall()
            res = []
            for row in results:
                line = {}
                inx = 0
                for col in row:
                    line[cur_des[inx][0]] = col
                    inx = inx + 1
                res.append(line)
            return res
        except Exception as e:
            self.db.rollback()
            raise e

    # 查询满足条件的第一条记录的值
    # 参数 字段名 表名 查询条件
    def query_value(self, value, table, condition="1=1"):
        cur = self.db.cursor()
        try:
            sql = "select " + value + " from " + table + " where " + str(condition)
            print(sql)
            cur.execute(sql)
            result = cur.fetchall()
            if len(result) > 0:
                return result[0]
            else:
                return None
        except Exception as e:
            self.db.rollback()
            raise e

    # 针对insert update delete操作
    def operator(self, sql):
        cur = self.db.cursor()
        try:
            cur.execute(sql)
            print(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    # 事务、存储过程等查询
    def operat_many(self, sqls):
        try:
            for sql in sqls:
                self.operator(sql)
        except Exception as e:
            self.db.rollback()
            raise e

    def __del__(self):
        self.db.close()



