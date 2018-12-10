from app.extensions import db
from datetime import datetime


class File(db.Model):
    __tablename__ = "File"
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, unique=True, autoincrement=True)
    # 文件名
    name = db.Column(db.String(64), nullable=False)
    # 文件类型
    type = db.Column(db.String(64), nullable=False, server_default="默认分类")
    # 上传者
    author = db.Column(db.String(256), nullable=False)
    # 上传日期
    pub_date = db.Column(db.DateTime, nullable=False, server_default=str(datetime.now()))
    # 文件物理路径
    path = db.Column(db.Text, nullable=False)
    # 访问控制
    # 以字符串形式存储的json
    # 格式 对属权限属于于group的用户或者用户名存在users中的用户开放
    # {"read":{"group":[],"users":[]},"edit":{"group":[],"users":[]}}
    authority = db.Column(db.Text)
    # 文件散列码
    hash = db.Column(db.String(128), nullable=False)
    # 下载量
    download = db.Column(db.Integer, nullable=False, server_default="0")
    # 文件状态 等待审核、审核通过、刊登、下架、删除
    status = db.Column(db.String(64), nullable=False, server_default="默认状态")

    def __repr__(self):
        return self.name[:64]
