import os
from flask import Blueprint, request, jsonify
from app.utils import SQL
from app.models import file
from app.config import Config, BASE_DIR


file = Blueprint("file", __name__)


@file.route('list', methods=['GET', 'POST'])
def get_list():
    pass


@file.route('download', methods=['GET', 'POST'])
def get_file():
    print(request.user_agent)
    print(request.remote_addr)
    return jsonify({"status": "ok"})


# 上传文件

# 文件名改为  文件名-hash.后缀  如果存在这个文件，则直接返回成功
# 参数
# 返回值 服务器文件路径
@file.route('upload', methods=['GET', 'POST'])
def rev_file():
    pass

    # 判断文件类别
    # param = request.form.get("type")
    # accestoken = request.form.get("accesstoken")
    # if param == "news":
    #     pass
    # if param == "123":
    #     f = request.files["file"]
    #
    #     f.filename
    #     f.save(os.path.join(Config.UPLOADED_DEST, f.filename))
    #     return jsonify({"status": "ok"})
    # else:
    #     return jsonify({"status": "false"})
