from app.extensions import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'User'
    # 账号
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, unique=True)
    # 昵称
    nickname = db.Column(db.String(45), server_default="未设置昵称")
    # 密码 这里的密码使用RSA加密
    password = db.Column(db.String(256), nullable=False)
    # 密码hash
    password_hash = db.Column(db.String(128), nullable=False)
    # accesstoken 最近登录使用的accesstoken
    access_token = db.Column(db.Text)
    # 最近登录时间
    latest_time = db.Column(db.DateTime)
    # 注册时间
    signin_time = db.Column(db.DateTime)
    # 用户权限
    # 此处的用户权限高于新闻、公告等写出的权限
    # {"read": ["news"], "edit": [], "upload":[], "approve":[], "delete":[]}
    authority = db.Column(db.Text)
    # 用户身份
    # 变更用户身份会自动更新用户权限
    # 具体分级见 app.views.config
    identity = db.Column(db.Integer, nullable=False, server_default="0")

    def __repr__(self):
        return self.nickname[:45]

    @staticmethod
    # 生成AccessToken
    # 参数 uid-用户ID
    def create_accesstoken(uid):
        import datetime
        import hashlib
        import random
        from app.utils import SQL
        s = SQL()
        password_hash = s.query_value("`password_hash`", "`user`", "`id`=" + uid)[0]
        # 获取当前时间并格式化为 日月年时分秒 如10122018151401
        time = datetime.datetime.now().strftime('%d%m%Y%H%M%S')
        # 将时间与用户账号连接 并进行一次MD5散列
        md5 = hashlib.md5()
        md5.update((time + uid).encode('utf-8'))  # 注意转码
        crypt1 = md5.hexdigest()

        # 将crypt1 和 密码的HASH值以及生成的随机数进行一次sha256
        random.seed()
        sha256 = hashlib.sha256()
        sha256.update(str(str(crypt1) + str(password_hash) + str(random.random())).encode('utf-8'))
        crypt2 = sha256.hexdigest()
        return crypt2

    @staticmethod
    # 生成用户权限
    def create_user_ahthority():
        return '{"read": [], "edit": [], "pub":[], "approve":[], "delete":[]}'

    @staticmethod
    # 通过access_token 记录查询ID
    def get_user_id(access_token="*"):
        from app.utils import SQL
        s = SQL()
        res = s.query_value("`id`", "`login`", "where `access_token` = '%s'" % access_token)
        if not res or len(res) < 1:
            return None
        return res[0]

    @staticmethod
    # 查询用户权限
    # uid
    # access_token
    def get_user_auth(uid=None, access_token=None):
        import datetime
        import json
        from flask import current_app
        from app.utils import SQL
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
            df = log[0] + datetime.timedelta(seconds=current_app.config["ACCESSTOKEN_VALID_TIME"])
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
