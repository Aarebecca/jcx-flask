from app import create_app
from flask_script import Manager
import os
from flask_migrate import MigrateCommand

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


# 从环境变量中获取config_name
config_name = os.environ.get('FLASK_CONFIG') or 'default'

# 生成app
app = create_app(config_name)

http_server = HTTPServer(WSGIContainer(app))

manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    http_server.listen(5000)
    IOLoop.instance().start()
    # manager.run()



