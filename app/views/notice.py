from flask import Blueprint, request, jsonify
from app.utils import SQL
from .utils import check_mani
from app.models import notice
from pymysql import escape_string
from app.log import Logger
notice = Blueprint('notice', __name__)
log = Logger("notice.log")


@notice.route("list", methods=['GET', 'POST'])
def get_list():
    try:
        page = int(request.args.get('page') or "1")
        psize = int(request.args.get('psize') or "8")
        pno = (page - 1) * psize
        s = SQL()
        condition = "where 1 = 1"
        sql = "select `id`,`pub_date`,`tag`,`title`,`type` from (select * from `notice` order by pub_date desc ) " \
              "tmp %s limit %d , %d " % (condition, pno, psize)
        return jsonify({"status": "ok", "data": s.query(sql)})
    except Exception as e:
        log.logger.warning(e)
        return jsonify({"status": "failed", "data": "error:%s" % e})


# 公告详情
# id
@notice.route("detail", methods=['GET', 'POST'])
def get_detail():
    try:
        nid = escape_string(request.args.get("id"))
        s = SQL()
        condition = "where id = %s" % nid
        sql = "select `id`,`title`,`pub_date`,`tag`,`author`,`type`,`content`,`read` from `notice` %s" % condition

        # 新闻阅读量+1
        sqls = [
            "begin work;",
            "select `read` from `notice` where `id` = '%s' for update;" % nid,
            "update `notice` set `read` = `read` + 1 where `id` = '%s';" % nid,
            "commit work;"
        ]
        s.operat_many(sqls)

        return jsonify({"status": "ok", "data": s.query(sql)})
    except Exception as e:
        log.logger.warning(e)
        return jsonify({"status": "failed", "data": "error:%s" % e})


# 上传公告
# 如果发布者权限大于等于管理员 则直接显示F
# 否则需要等待管理员审核新闻后才可显示
@notice.route('publish', methods=['GET', 'POST'])
def rev_news():
    try:
        # 为作者分配修改、删除权限
        accesstoken = request.form.get("accesstoken")
        if check_mani("pub", "news", accesstoken=accesstoken) is True:
            print("YES")

    except Exception as e:
        log.logger.warning(e)
        return jsonify({"status": "failed", "data": "error:%s" % e})


# 修改公告
@notice.route('edit', methods=['GET', 'POST'])
def rev_edit():
    try:
        accesstoken = request.form.get("accesstoken")
        check_mani()
        pass
    except Exception as e:
        log.logger.warning(e)
        return jsonify({"status": "failed", "data": "error:%s" % e})


# 公告审批
@notice.route('review', methods=['GET', 'POST'])
def news_review():
    try:
        pass
    except Exception as e:
        log.logger.warning(e)
        return jsonify({"status": "failed", "data": "error:%s" % e})

