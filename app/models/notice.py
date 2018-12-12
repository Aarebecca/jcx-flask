from app.extensions import db
from datetime import datetime


class Notice(db.Model):
    __tablename__ = "Notice"
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, unique=True, autoincrement=True)
    # 标题
    title = db.Column(db.String(64), nullable=False)
    # 发布日期
    pub_date = db.Column(db.DateTime)
    # 公告通知标签 如new hot
    tag = db.Column(db.String(16))
    # 公告通知发布者
    author = db.Column(db.String(256), nullable=False)
    # 发布者ID
    publisher = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    # 访问控制
    # 以字符串形式存储的json
    # 格式 对属权限属于于group的用户或者用户名存在users中的用户开放
    # {"read":{"group":[],"users":[]},"edit":{"group":[],"users":[]}}
    authority = db.Column(db.Text)
    # 公告内容
    content = db.Column(db.Text, nullable=False)
    # 阅读量
    read = db.Column(db.Integer, nullable=False, server_default="0")
    # 公告类别
    type = db.Column(db.String(64), nullable=False, server_default="默认分类")
    # 公告状态 等待审核、审核通过、刊登、下架、删除
    status = db.Column(db.String(64), nullable=False, server_default="默认状态")

    def __repr__(self):
        return self.title[:64]
