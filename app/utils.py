import math
import pymysql
from app.config import ProductionConfig as pr


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
        self.db = pymysql.connect(host=pr.SQL_HOST, user=pr.SQL_USER, password=pr.SQL_PSW, database=pr.SQL_DB,
                                  port=pr.SQL_PORT)

    def query(self, sql):
        cur = self.db.cursor()
        try:
            cur.execute(sql)
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
            raise e

    def operator(self, sql):
        cur = self.db.cursor()
        try:
            cur.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()

    def __del__(self):
        self.db.close()








