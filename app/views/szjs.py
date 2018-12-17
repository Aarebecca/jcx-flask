from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import people
from pymysql import escape_string
from app.utils import SQL
from app.log import Logger
sz = Blueprint('szjs', __name__)
log = Logger("sz.log")


# 师资团队列表
# 人数多的情况下可以按页查询
@sz.route('list', methods=['GET', 'POST'])
def get_list():
    try:
        page = int(request.args.get('page') or "1")
        psize = int(request.args.get('psize') or "50")
        pno = (page - 1) * psize
        s = SQL()
        # 按职称分别查询
        job = ["教授", "副教授", "讲师", "其他"]
        res = {}
        for t in job:
            condition = "where job = '%s'" % t
            sql = "select `id`,`name`,`header`,`job` from `people` where `job` = '%s';" % t
            res[t] = s.query(sql)
        return jsonify({"status": "ok", "data": res})
    except Exception as e:
        log.logger.warning(e)
        return jsonify({"status": "failed", "data": "error:%s" % e})


# 根据id获取具体详情
# id
@sz.route('detail', methods=['GET', 'POST'])
def get_detail():
    try:
        tid = escape_string(request.args.get("id"))
        s = SQL()
        condition = "where id = %s" % tid
        sql = "select `name`,`homepage`,`header`,`age`,`job`,`edu`,`degree`,`email`,`native`,`pho`,`department`," \
              "`intro`,`paper`,`other` from `people` where id = %s;" % tid
        return jsonify({"status": "ok", "data": s.query(sql)})
    except Exception as e:
        log.logger.warning(e)
        return jsonify({"status": "failed", "data": "error:%s" % e})


# 编辑师资介绍
@sz.route('edit', methods=['POST'])
def edit_abs():
    try:
        import os
        from app.config import BASE_DIR
        # 身份验证

        content = request.args.get("abstract")
        f = open(os.path.join(BASE_DIR, "data/sz.txt"), 'w')
        f.write(content)
        f.close()
        return jsonify({"status": "ok", "data": "修改成功！"})
    except Exception as e:
        log.logger.warning(e)
        return jsonify({"status": "failed", "data": "error:%s" % e})


# 师资介绍大概
@sz.route('abstract', methods=['GET', 'POST'])
def get_abs():
    try:
        import os
        from app.config import BASE_DIR

        f = open(os.path.join(BASE_DIR, "data/sz.txt"), 'r')
        text = f.read()
        f.close()
        s = SQL()
        sql = "select (select count(id) from `people`) 'total',(select count(id) from `people` where job = '教授') " \
              "'pro',(select count(id) from `people` where job = '副教授') 'ass'"
        res = s.query(sql)[0]
        print(res)
        print(text)
        text = text.replace("{{total}}", str(res["total"])).replace("{{pro}}", str(res["pro"]))\
            .replace("{{ass}}", str(res["ass"]))
        return jsonify({"status": "ok", "data": text})
    except Exception as e:
        log.logger.warning(e)
        return jsonify({"status": "failed", "data": "error:%s" % e})


# 添加人员详情
@sz.route('add', methods=['GET', 'POST'])
def add_people():
    try:
        pass
    except Exception as e:
        log.logger.warning(e)
        return jsonify({"status": "failed", "data": "error:%s" % e})