import logging
from logging import handlers
from .config import Config
import os


# 日志级别关系映射
class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, filename, level='info', when='D', backcount=3,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        filename = os.path.join(Config.LOG_STORE_PATH, filename)
        self.logger = logging.getLogger(filename)
        # 设置日志格式
        format_str = logging.Formatter(fmt)
        # 设置日志级别
        self.logger.setLevel(self.level_relations.get(level))
        # 往屏幕上输出
        sh = logging.StreamHandler()
        # 设置屏幕上显示的格式
        sh.setFormatter(format_str)
        # 往文件里写入#指定间隔时间自动生成文件的处理器
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backcount, encoding='utf-8')
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        # 设置文件里写入的格式
        th.setFormatter(format_str)
        # 把对象加到logger里
        self.logger.addHandler(sh)
        self.logger.addHandler(th)


if __name__ == '__main__':
    pass
    # log = Logger('all.log', level='debug')
    # log.logger.debug('debug')
    # log.logger.info('info')
    # log.logger.warning('警告')
    # log.logger.error('报错')
    # log.logger.critical('严重')
    # Logger('error.log', level='error').logger.error('error')
