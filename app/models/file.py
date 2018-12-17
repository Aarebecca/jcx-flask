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
    pub_date = db.Column(db.DateTime)
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

    @staticmethod
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

    @staticmethod
    # 生成对象访问权限
    # 用户自定的策略
    def create_obj_ahthority(strategy=None):
        return '{"read":{"identity":[],"users":[]},"edit":{"identity":[],"users":[]}}'
