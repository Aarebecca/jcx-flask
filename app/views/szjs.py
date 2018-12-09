from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import people

from app.utils import SQL

sz = Blueprint('szjs', __name__)


@sz.route('list', methods=['GET', 'POST'])
def get_list():
    pass


@sz.route('detail', methods=['GET', 'POST'])
def get_detail():
    pass
