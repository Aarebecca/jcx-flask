from flask import Blueprint, request, jsonify
from app.utils import SQL


utils = Blueprint("utils", __name__)


# 获取开启的模块列表
@utils.route("module", methods=["GET", "POST"])
def get_module():
    pass
