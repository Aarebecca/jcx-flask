from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import user, login
from app.log import Logger
from app.utils import SQL
from pymysql import escape_string

users = Blueprint('users', __name__)
log = Logger("user.log")


@users.route('/query', methods=['GET', 'POST'])
def index():
    try:
        s = SQL()
        sql = "select * from `user`"
        return jsonify({"status": "ok", "data": s.query(sql)})
    except Exception as e:
        log.logger.warning(e)
        return jsonify({"status": "failed", "data": "error:%s" % e})


# 注册、添加用户
# 账号
# 密码
# 验证码
@users.route('/add', methods=['GET', 'POST'])
def add_user():
    try:
        pass
    except Exception as e:
        log.logger.warning(e)
        return jsonify({"status": "failed", "data": "error:%s" % e})


# 账号
# 密码hash值
# 验证码
@users.route('/login', methods=['POST'])
def user_login():
    import hashlib
    from datetime import datetime
    try:
        uid = escape_string(request.args.get("id")) or None
        password_hash = escape_string(request.args.get("password_hash")) or None
        code = escape_string(request.args.get("code") or "")
        usa = request.user_agent or "hidden"
        uip = request.remote_addr or "hidden"

        # md5 = hashlib.md5()
        # md5.update(password.encode("utf-8"))
        # password_hash = md5.hexdigest()

        s = SQL()
        if password_hash == s.query_value("`password_hash`", "`user`", "`id`='%s'" % uid)[0]:
            # 验证通过

            # 生成token
            token = user.User.create_accesstoken(uid)

            # 存入登录记录
            lgn = login.Login(uid=uid, time=datetime.now(), ip=uip, user_agent=usa,
                              access_token=token, mani="login")
            db.session.add(lgn)
            db.session.commit()

            # 更新user表
            s = SQL()
            sql = "update `user` set `latest_time`='%s', `access_token`='%s' where `id`='%s'" % (datetime.now(), token, uid)
            s.operator(sql)

            return jsonify({"status": "ok", "data": token})
        else:
            # 密码或账号错误
            return jsonify({"status": "failed", "data": "密码或账号错误"})
    except Exception as e:
        log.logger.warning(e)
        return jsonify({"status": "failed", "data": "error:%s" % e})
