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

    # 查询满足条件的第一条记录的值
    # 参数 字段名 表名 查询条件
    def query_value(self, value, table, condition="1=1"):
        cur = self.db.cursor()
        try:
            sql = "select " + value + " from " + table + " where " + str(condition)
            cur.execute(sql)
            result = cur.fetchall()
            print(type(result))
            if len(result) > 0:
                return result[0]
            else:
                return None
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


# 用户操作权限查询
# 参数 用户操作 accesstoken
# 操作类型
# mani  操作 pub read eidt delete 等
# obj 对象表  news notice file 等
# oid 对象编号
# access_token 用户access_token
# user表中 access_token 字段默认为空，故取其值为*以避免查询错误
def check_mani(mani, obj, oid=None, access_token="*"):
    import json
    s = SQL()

    # 根据access_token查询用户
    user = s.query_value("`id`,`authority`,`identity`", "`user`", "`access_token`=" + access_token)
    auth_user = json.loads(user[1])

    # 发布、上传
    if mani == "pub":
        for iobj in auth_user["pub"]:
            if iobj == obj:
                return True

    # 查询、修改
    # 查询访问权限
    auth_obj = json.loads(s.query_value("`authority`", "`" + obj + "`", "`id`=" + oid)[0])

    # 如果请求的资源为read并且对所有人可见,则可以访问
    for index in auth_obj["read"]["identity"]:
        if index == "everyone" and mani == "read":
            return True

    # 用户身份不通过
    if user is None:
        return False
    # 查询其操作权限
    else:
        # 用户的管理员身份通过

        for mani_type in auth_user:
            # 查询操作权限
            if mani_type == mani:
                # 查询权限是否存在
                for iobj in auth_user[mani_type]:
                    if iobj == obj:
                        return True

        # 用户在obj许可中
        # 用户在identity中
        for iden in auth_obj[mani]["identity"]:
            if iden == "public" or int(iden) >= int(user[2]):
                return True
        # 用户在users中
        for users in auth_obj[mani]["users"]:
            if users == user[0]:
                return True
    # 其他情况
    return False


# 生成AccessToken
# 参数 uid-用户ID
def create_accesstoken(uid):
    import datetime
    import hashlib
    import random
    s = SQL()
    password_hash = s.query_value("`password_hash`", "`user`", "`id`="+uid)[0]
    # 获取当前时间并格式化为 日月年时分秒 如10122018151401
    time = datetime.datetime.now().strftime('%d%m%Y%H%M%S')
    # 将时间与用户账号连接 并进行一次MD5散列
    md5 = hashlib.md5()
    md5.update((time+uid).encode('utf-8'))  # 注意转码
    crypt1 = md5.hexdigest()

    # 将crypt1 和 密码的HASH值以及生成的随机数进行一次sha256
    random.seed()
    sha256 = hashlib.sha256()
    sha256.update(str(str(crypt1)+str(password_hash)+str(random.random())).encode('utf-8'))
    crypt2 = sha256.hexdigest()
    return crypt2
