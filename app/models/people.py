# 院内用户人员信息表
from app.extensions import db


class People(db.Model):
    __tablename__ = "People"
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, unique=True, autoincrement=True)
    # 工号、学号
    no = db.Column(db.Integer, unique=True)
    # 姓名
    name = db.Column(db.String(64), nullable=False)
    # 个人主页链接
    homepage = db.Column(db.Text)
    # 年龄
    age = db.Column(db.Integer)
    # 职位
    job = db.Column(db.String(32))
    # 学历
    edu = db.Column(db.String(32))
    # 学位
    degree = db.Column(db.String(32))
    # 电子邮箱
    email = db.Column(db.String(256))
    # 籍贯
    native = db.Column(db.String(32))
    # 电话
    pho = db.Column(db.String(20))
    # 部门
    department = db.Column(db.String(32))
    # 介绍
    intro = db.Column(db.Text)
    # 论文及专著
    paper = db.Column(db.Text)
    # 其他介绍
    other = db.Column(db.Text)

    def __repr__(self):
        return self.name[:64]
