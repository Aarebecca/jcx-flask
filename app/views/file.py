from flask import Blueprint, request, jsonify
from app.utils import SQL
from app.models import file
import os

file = Blueprint("file", __name__)


@file.route('list', methods=['GET', 'POST'])
def get_list():
    pass


@file.route('download', methods=['GET', 'POST'])
def get_file():
    return jsonify({"status": "ok"})


# 上传文件
@file.route('upload', methods=['GET', 'POST'])
def rev_file():
    param = request.form.get("n")
    if param == "123":
        f = request.files["file"]
        f.save(os.path.dirname(__file__)+'/../asset/upload/'+f.filename)
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "false"})