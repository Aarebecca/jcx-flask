from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import user

from app.utils import SQL

users = Blueprint('users', __name__)


@users.route('/query', methods=['GET', 'POST'])
def index():
    s = SQL()
    sql = "select * from `user`"
    return jsonify({"status": "ok", "data": s.query(sql)})


@users.route('/add', methods=['GET', 'POST'])
def add_user():
    pass