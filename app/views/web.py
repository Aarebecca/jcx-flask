from flask import Blueprint, request, jsonify, render_template
web = Blueprint('web', __name__)


@web.route('/', methods=['GET', 'POST'])
def index():
    context = {
        'logoURL': "../static/assets/images/logo.png"
    }
    return render_template("index.html", **context)


@web.route('/<string:html>', methods=['GET', 'POST'])
def getweb(html):
    return render_template(html)
