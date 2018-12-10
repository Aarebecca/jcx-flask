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
    access_token = db.Column(db.Text, unique=True)
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
