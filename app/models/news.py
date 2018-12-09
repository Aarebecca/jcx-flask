from app.extensions import db
from datetime import datetime


class News(db.Model):
    __tablename__ = "News"
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, unique=True, autoincrement=True)
    # 标题
    title = db.Column(db.String(64), nullable=False)
    # 发布日期
    pub_date = db.Column(db.DateTime, nullable=False, server_default=str(datetime.now()))
    # 新闻摘要
    abstract = db.Column(db.Text)
    # 新闻内容HTML
    content = db.Column(db.Text, nullable=False)
    # 封面照片链接
    album = db.Column(db.String(256))
    # 作者
    author = db.Column(db.String(256), nullable=False)
    # 阅读量
    read = db.Column(db.Integer, nullable=False, server_default="0")
    # 新闻类别
    type = db.Column(db.String(64), nullable=False, server_default="默认分类")
    # 新闻状态 等待审核、审核通过、刊登、下架、删除
    status = db.Column(db.String(64), nullable=False, server_default="默认状态")

    def __repr__(self):
        return self.title[:64]
