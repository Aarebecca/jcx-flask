from app.extensions import db
from datetime import datetime


class Notice(db.Model):
    __tablename__ = "Notice"
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, unique=True, autoincrement=True)
    # 标题
    title = db.Column(db.String(64), nullable=False)
    # 发布日期
    pub_date = db.Column(db.DateTime, nullable=False, server_default=str(datetime.now()))
    # 公告通知标签 如new hot
    tag = db.Column(db.String(16))
    # 公告通知发布者
    author = db.Column(db.String(256), nullable=False)
    # 公告内容
    content = db.Column(db.Text, nullable=False)
    # 阅读量
    read = db.Column(db.Integer, nullable=False, server_default="0")
    # 公告状态 等待审核、审核通过、刊登、下架、删除
    type = db.Column(db.String(64), nullable=False, server_default="默认状态")

    def __repr__(self):
        return self.title[:64]
