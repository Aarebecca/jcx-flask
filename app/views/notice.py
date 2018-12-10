from flask import Blueprint, request, jsonify
from app.utils import SQL, check_mani
from app.models import notice

notice = Blueprint('notice', __name__)


@notice.route("list", methods=['GET', 'POST'])
def get_list():
    page = int(request.args.get('page') or "1")
    psize = int(request.args.get('psize') or "8")
    pno = (page-1)*psize
    s = SQL()
    condition = " where 1 = 1"
    sql = "select * from (select * from `notice` order by pub_date desc ) tmp" + condition + " limit "\
          + str(pno) + "," + str(psize)
    return jsonify({"status": "ok", "data": s.query(sql)})


@notice.route("detail", methods=['GET', 'POST'])
def get_detail():
    nid = request.args.get("id")
    s = SQL()
    condition = " where id = {c_id}".format(c_id=nid)
    sql = "select * from `notice`" + condition
    return jsonify({"status": "ok", "data": s.query(sql)})


# 上传公告
# 如果发布者权限大于等于管理员 则直接显示
# 否则需要等待管理员审核新闻后才可显示
@notice.route('publish', methods=['GET', 'POST'])
def rev_news():
    # 为作者分配修改、删除权限
    accesstoken = request.form.get("accesstoken")
    if check_mani("pub", "news", accesstoken=accesstoken) is True:
        print("YES")


# 修改公告
@notice.route('edit', methods=['GET', 'POST'])
def rev_edit():
    accesstoken = request.form.get("accesstoken")
    check_mani()
    pass


# 公告审批
@notice.route('review', methods=['GET', 'POST'])
def news_review():
    pass
