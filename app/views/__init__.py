from .news import news
from .user import users
from .notice import notice
from .file import file
from .szjs import sz

DEFAULT_BLUEPRINT = (
    (news, '/news/'),
    (users, '/user/'),
    (notice, '/notice/'),
    (file, '/file/'),
    (sz, '/sz/')
)


# 封装配置蓝本的函数
def config_blueprint(app):
    # 循环读取元组中的蓝本
    for blueprint, prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint, url_prefix=prefix)
