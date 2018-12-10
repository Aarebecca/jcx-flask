from app.extensions import db
from datetime import datetime


class Login(db.Model):
    __tablename__ = "Login"
    # 操作编号
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, unique=True, autoincrement=True)
    # 账号
    uid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # 时间
    time = db.Column(db.DateTime)
    # IP
    ip = db.Column(db.String(46), nullable=False)
    # user_agent
    user_agent = db.Column(db.Text)
    # AccessToken
    access_token = db.Column(db.Text)
    # 操作
    mani = db.Column(db.Text)

    def __repr__(self):
        return self.uid[:64]
