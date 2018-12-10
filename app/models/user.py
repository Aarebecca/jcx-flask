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
    # {"read": ["news"], "edit": [], "upload":[], "approve":[]}
    authority = db.Column(db.String(16), nullable=False, server_default="default")
    # 用户身份
    identity = db.Column(db.String(16), nullable=False, server_default="default")

    def __repr__(self):
        return self.nickname[:45]
