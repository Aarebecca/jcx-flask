from app.utils import SQL
import json


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


# 通过access_token 记录查询ID
def get_user_id(access_token="*"):
    s = SQL()
    res = s.query_value("`id`", "`login`", "where `access_token` = '%s'" % access_token)
    if not res or len(res) < 1:
        return None
    return res[0]


# 查询用户权限
# uid
# access_token
def get_user_auth(uid=None, access_token=None):
    import datetime
    from app.config import Config
    s = SQL()
    sql = ""
    user = None
    if uid is not None:
        user = s.query_value("`authority`", "`user`", "`id`=" + uid)
    # 使用accesstoken 需要验证时效性
    elif access_token is not None:
        # 取用户最近一次操作
        log = s.query_value("`time`,`mani`", "`login`",
                            "access_token = '%s' order by time desc limit 1;" % access_token)
        # token无效
        if not log:
            print("查询结果为空")
            return False
        # 如果是注销 logout 则需要重新登录
        # 如果access token过期
        df = log[0] + datetime.timedelta(seconds=Config.ACCESSTOKEN_VALID_TIME)
        if log[1] == "logout" or df < datetime.datetime.now():
            print("accesstoken过期")
            return False
        user = s.query_value("`authority`", "`user`", "`access_token`='%s'" % access_token)
    else:
        return False
    # 查询不到结果
    if not user or len(user) < 1:
        return False
    return json.loads(user[0])


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


# 计算文件hash值
def cul_file_hash(fp):
    import hashlib
    _FILE_SLIM = (100 * 1024 * 1024)  # 100MB
    md5 = hashlib.md5()
    f_size = len(fp.read())
    # 重置文件指针
    fp.seek(0, 0)
    if f_size > _FILE_SLIM:
        while f_size > _FILE_SLIM:
            md5.update(fp.read(_FILE_SLIM))
    f_size /= _FILE_SLIM
    if (f_size > 0) and (f_size <= _FILE_SLIM):
        md5.update(fp.read())
    else:
        md5.update(fp.read())
    # 重置文件指针
    fp.seek(0, 0)
    return md5.hexdigest()


# 生成对象访问权限
# 用户自定的策略
def create_obj_ahthority(strategy=None):
    return '{"read":{"identity":[],"users":[]},"edit":{"identity":[],"users":[]}}'


# 生成用户权限
def create_user_ahthority():
    return '{"read": [], "edit": [], "pub":[], "approve":[], "delete":[]}'
