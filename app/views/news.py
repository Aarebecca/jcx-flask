from flask import Blueprint, request, jsonify
from app.utils import SQL
from .utils import get_user_auth
from app.models.news import News

news = Blueprint('news', __name__)


# 获取新闻列表
# 新闻类别
# page - 新闻页数
# psize - 每页条数
@news.route('list', methods=['GET', 'POST'])
def get_list():
    page = int(request.args.get('page') or "1")
    psize = int(request.args.get('psize') or "8")
    ntype = request.args.get("type") or "news"

    pno = (page - 1) * psize
    s = SQL()
    # 补充查询条件
    condition = " where 1 = 1 and `status` = 'valid' and `type` = '%s'" % ntype
    sql = "select `id`,`title`,`pub_date`,`album`,`author`,`type` from " \
          "(select * from `news` order by pub_date desc ) tmp %s limit %d , %d" % (condition, pno, psize)
    return jsonify({"status": "ok", "data": s.query(sql)})


# 管理员获取新闻列表
# page - 新闻页数
# psize - 每页条数
# accesstoken
@news.route('mlist', methods=['GET', 'POST'])
def get_mlist():
    page = int(request.args.get('page') or "1")
    psize = int(request.args.get('psize') or "8")
    pno = (page - 1) * psize
    s = SQL()
    # 补充查询条件
    condition = "where 1 = 1 and `status` = 'valid'"
    sql = "select `id`,`title`,`pub_date`,`album`,`author`,`type` from " \
          "(select * from `news` order by pub_date desc ) tmp %s limit %d , %d" % (condition, pno, psize)
    return jsonify({"status": "ok", "data": s.query(sql)})


# 根据新闻id获取具体详情
# id - 新闻id
@news.route('detail', methods=['GET', 'POST'])
def get_detail():
    newid = request.args.get("id")
    s = SQL()
    condition = "where id = %s" % newid
    sql = "select `id`,`title`,`pub_date`,`abstract`,`content`,`album`,`author`,`read`,`type` from `news` %s" \
          % condition

    # 新闻阅读量+1
    sqls = [
        "begin work;",
        "select `read` from `news` where `id` = '%s' for update;" % newid,
        "update `news` set `read` = `read` + 1 where `id` = '%s';" % newid,
        "commit work;"
    ]
    s.operat_many(sqls)

    return jsonify({"status": "ok", "data": s.query(sql)})


# 上传新闻
# 如果发布者权限大于等于管理员 则直接显示
# 否则需要等待管理员审核新闻后才可显示
# accesstoken
@news.route('publish', methods=['GET', 'POST'])
def rev_news():
    access_token = request.form.get("accesstoken")

    # 权限验证通过之后

    # 返回新闻ID


# 修改新闻
# id - 新闻id
# access_token
@news.route('edit', methods=['POST'])
def rev_edit():
    from .utils import get_obj_auth, create_obj_ahthority,get_user_id
    from datetime import datetime
    t = request.args
    access_token = t.get("accesstoken")
    nid = t.get("id")
    # 获取新闻权限信息
    obj_auth = get_obj_auth(oid=nid,obj="news")
    if not obj_auth:
        # 无此条新闻或者权限信息
        return jsonify({"status": "failed", "data": "无权限！"})
    # 验证权限
    # get_user_auth

    # 权限验证通过之后


    # 存入新闻
    nnews = News(title=t.get("title"), pub_date=datetime.now(), abstract=t.get("abstract"), content=t.get("content"),
                 album=t.get("album"), author=t.get("author"), authority=create_obj_ahthority(), type=t.get("type"),
                 read="0", status="pending", publisher=get_user_id(access_token=access_token))



# 新闻审批
# access_token
# id
@news.route('review', methods=['GET', 'POST'])
def news_review():


    # 通过验证
