from flask import Blueprint, request, jsonify
from app.utils import SQL
from .utils import get_user_auth
from app.models import news

news = Blueprint('news', __name__)


# 获取新闻列表
# page - 新闻页数
# psize - 每页条数
@news.route('list', methods=['GET', 'POST'])
def get_list():
    page = int(request.args.get('page') or "1")
    psize = int(request.args.get('psize') or "8")
    pno = (page - 1) * psize
    s = SQL()
    # 补充查询条件
    condition = " where 1 = 1 and `status` = 'valid'"
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
    return jsonify({"status": "ok", "data": s.query(sql)})


# 上传新闻
# 如果发布者权限大于等于管理员 则直接显示
# 否则需要等待管理员审核新闻后才可显示
# accesstoken
@news.route('publish', methods=['GET', 'POST'])
def rev_news():
    access_token = request.form.get("accesstoken")



# 修改新闻
# id - 新闻id
@news.route('edit', methods=['GET', 'POST'])
def rev_edit():
    pass


# 新闻审批
@news.route('review', methods=['GET', 'POST'])
def news_review():
    pass
