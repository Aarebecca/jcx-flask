from app.utils import SQL
import json


# 查询新闻、公告、文件等权限
# oid
# obj
def get_obj_auth(oid=None, obj=None):
    s = SQL()
    if obj is None:
        return False
    res = s.query_value("`authority`", "`" + obj + "`", "`id`=" + oid)
    if not res or len(res) < 1:
        return False
    return json.loads(res[0])


# 用户操作权限查询
# 参数 用户操作 accesstoken
# 操作类型
# mani  操作 pub read eidt delete 等
# obj 对象表  news notice file 等
# oid 对象编号
# access_token 用户access_token
# user表中 access_token 字段默认为空，故取其值为*以避免查询错误
def check_mani(mani, obj, oid=None, access_token="*"):
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




