from flask import Blueprint, request, jsonify
from app.utils import SQL
from app.models import news

news = Blueprint('news', __name__)


# 获取新闻列表
# page - 新闻页数
# psize - 每页条数
@news.route('list', methods=['GET', 'POST'])
def get_list():
    page = request.args.get('page') or "1"
    psize = request.args.get('psize') or "8"
    s = SQL()
    sql = "call `newslist`(" + page + "," + psize + ")"
    return jsonify({"status": "ok", "data": s.query(sql)})


# 根据新闻id获取具体详情
# id - 新闻id
@news.route('detail', methods=['GET', 'POST'])
def get_detail():
    newid = request.args.get("id")
    s = SQL()
    sql = "select * from `news` where id = " + newid
    return jsonify({"status": "ok", "data": s.query(sql)})
