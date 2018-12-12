from app.extensions import db
from datetime import datetime


class News(db.Model):
    __tablename__ = "News"
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, unique=True, autoincrement=True)
    # 标题
    title = db.Column(db.String(64), nullable=False)
    # 发布日期
    pub_date = db.Column(db.DateTime)
    # 新闻摘要
    abstract = db.Column(db.Text)
    # 新闻内容HTML
    content = db.Column(db.Text, nullable=False)
    # 封面照片链接
    album = db.Column(db.String(256))
    # 作者
    author = db.Column(db.String(256), nullable=False)
    # 发布者ID
    publisher = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    # 访问控制
    # 以字符串形式存储的json
    # 格式 对属权限属于于group的用户或者用户名存在users中的用户开放
    # {"read":{"identity":[],"users":[]},"edit":{"identity":[],"users":[]}}
    # 特别定义
    # everyone - 对所有人可见，包括匿名用户,【注：只有read属性可以分配everyone】
    # public - 对登录的所有用户
    # nobody - 对权限低于自己的人不可见，管理员等仍可查看
    authority = db.Column(db.Text)
    # 阅读量
    read = db.Column(db.Integer, nullable=False, server_default="0")
    # 新闻类别
    type = db.Column(db.String(64), nullable=False, server_default="默认分类")
    # 新闻状态 等待审核-pending、审核通过刊登-pass、封存-block、下架、删除-delete
    status = db.Column(db.String(64), nullable=False, server_default="默认状态")

    def __repr__(self):
        return self.title[:64]
