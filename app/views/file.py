import os
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from app.utils import SQL
from app.models.file import File
from app.models.user import User
from app.models.login import Login
from app.config import BASE_DIR
from pymysql import escape_string
from app.log import Logger

file = Blueprint("file", __name__)
log = Logger("file.log")


# [accesstoken]
# [format] 文件格式
@file.route('list', methods=['GET', 'POST'])
def get_list():
    try:
        pass
        # 权限鉴定
    except Exception as e:
        log.logger.warning(e)
        return jsonify({"status": "failed", "data": "错误请求"})


@file.route('download', methods=['GET', 'POST'])
def get_file():
    try:
        from .utils import get_obj_auth

        oid = escape_string(request.args.get("id"))
        s = SQL()
        # 文件不存在
        file_res = s.query_value("`*`", "`file`", "id='%s'" % oid)
        if file_res is None or len(file_res) < 1:
            return jsonify({"status": "failed", "data": {"code": 1, "msg": "文件不存在！"}})

        # 文件权限查询

        # 查询文件路径
        file_path = s.query_value("`path`", "`file`", "`id`='%s'" % oid)[0]

        file_abpath = os.path.join(BASE_DIR, file_path)

        # 下载次数 + 1

        sqls = [
            "begin work;",
            "select `download` from `file` where `id` = '%s' for update;" % oid,
            "update `file` set `download` = `download` + 1 where `id` = '%s';" % oid,
            "commit work;"
        ]
        s.operat_many(sqls)

        # 记录用户操作
        print(request.user_agent)
        print(request.remote_addr)
        f_dic, fn = os.path.split(file_abpath)
        return send_from_directory(directory=f_dic, filename=fn, as_attachment=True)
    except Exception as e:
        log.logger.warning(e)
        return jsonify({"status": "failed", "data": "错误请求"})


# 上传文件

# 文件名改为  文件名-文件归属-hash.后缀  如果存在这个文件，则直接返回成功
# 参数
# accesstoken
# type
#
# 返回值 服务器文件路径
@file.route('upload', methods=['POST'])
def rev_file():
    try:
        from werkzeug.utils import secure_filename
        import datetime
        from app.extensions import db
        accesstoken = request.form.get('accesstoken')
        # 定义返回参数
        file_url = ""

        # 接收部分参数
        obj = request.form.get('type') or "None"

        # 权限控制
        user_auth = User.get_user_auth(access_token=accesstoken)
        print(user_auth)
        if not user_auth or obj not in user_auth["pub"]:
            return jsonify({"status": "failed", "data": {"code": 1, "msg": "你无权限上传文件！"}})

        # 接收文件
        f = request.files["file"] or None
        if f is None:
            return jsonify({"status": "failed", "data": {"code": 2, "msg": "未接收到文件！"}})

        # 取文件名和后缀
        fn, ff = os.path.splitext(secure_filename(f.filename))
        # 格式控制
        if str.lower(ff) not in current_app.config["ALLOWED_FILE_FORMAT"]:
            return jsonify({"status": "failed", "data": {"code": 3, "msg": "不允许的文件格式！"}})

        # 文件大小
        f_size = len(f.read())
        # 重置文件指针
        f.seek(0, 0)
        if f_size > current_app.config["MAX_FILE_SIZE"]:
            return jsonify({"status": "failed", "data": {"code": 4, "msg": "文件过大！"}})

        # 文件查重
        file_hash = File.cul_file_hash(f)
        s = SQL()
        query_res = s.query_value("`path`", "`file`", "`hash`='%s'" % file_hash)

        uid = s.query_value("`id`", "`user`", "access_token='%s'" % accesstoken)[0]
        # 文件未收录
        if query_res is None or len(query_res) < 1:
            # 文件名安全性  werzeug

            basepath = current_app.config["UPLOADED_TMP_DEST"]
            if obj == "news":
                basepath = current_app.config["UPLOADED_NEWS_DEST"]
                file_url = os.path.join(current_app.config["UPLOADED_BASE_DIR"], 'news')
            elif obj == "notice":
                basepath = current_app.config["UPLOADED_NOTICE_DEST"]
                file_url = os.path.join(current_app.config["UPLOADED_BASE_DIR"], 'notice')
            elif obj == "file":
                basepath = current_app.config["UPLOADED_FILE_DEST"]
                file_url = os.path.join(current_app.config["UPLOADED_BASE_DIR"], 'file')
            elif obj == "person":
                basepath = current_app.config["UPLOADED_FILE_DEST"]
                file_url = os.path.join(current_app.config["UPLOADED_BASE_DIR"], 'person')
            else:
                basepath = current_app.config["UPLOADED_TMP_DEST"]
                file_url = os.path.join(current_app.config["UPLOADED_BASE_DIR"], 'tmp')

            filename = fn + "-" + obj + "-" + file_hash + ff
            filepath = os.path.join(basepath, filename)
            # 存入目录
            f.save(filepath)
            file_url = os.path.join(file_url, filename)

            #
            #
            # 设置文件权限
            # 如果不是公开文件，就要设置动态下载
            #

            # 数据库存档
            new_file = File(name=filename, type=ff, author=uid, pub_date=datetime.datetime.now(), path=file_url
                            , authority=File.create_obj_ahthority(), hash=file_hash, status="default")
            db.session.add(new_file)
            db.session.commit()

        # 文件已收录，返回文件路径
        else:
            # 返回文件路径
            file_url = query_res[0]
        # 记录用户操作记录
        uip = request.remote_addr or "hidden"
        usa = str(request.user_agent) or "hidden"
        lgn = Login(uid=uid, time=datetime.datetime.now(), ip=uip, user_agent=usa, access_token=accesstoken,
                    mani="upload file: %s" % file_url)
        db.session.add(lgn)
        db.session.commit()

        return jsonify({"status": "ok", "data": {"url": file_url}})
    except Exception as e:
        log.logger.warning(e)
        return jsonify({"status": "failed", "data": "错误请求"})
