from flask import Blueprint, request, jsonify
from app.utils import SQL
from app.models import notice

notice = Blueprint('notice', __name__)


@notice.route("list", methods=['GET', 'POST'])
def get_list():
    page = request.args.get('page') or "1"
    psize = request.args.get('psize') or "8"
    s = SQL()
    sql = "call `noticelist`(" + page + "," + psize + ")"
    return jsonify({"status": "ok", "data": s.query(sql)})


@notice.route("detail", methods=['GET', 'POST'])
def get_detail():
    nid = request.args.get("id")
    s = SQL()
    sql = "select * from `notice` where id = " + nid
    return jsonify({"status": "ok", "data": s.query(sql)})

