from .news import news
from .user import users
from .notice import notice
from .utils import utils
from .file import file

DEFAULT_BLUEPRINT = (
    (news, '/news/'),
    (users, '/user/'),
    (notice, '/notice/'),
    (utils, '/utils/'),
    (file, '/file/')
)


# 封装配置蓝本的函数
def config_blueprint(app):
    # 循环读取元组中的蓝本
    for blueprint, prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint, url_prefix=prefix)
