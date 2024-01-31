from loguru import logger
import os

loggers_container = {}

LOG_ENABLED = True  # 是否开启日志
LOG_TO_CONSOLE = True  # 是否输出到控制台
LOG_TO_FILE = True  # 是否输出到文件
LOG_FORMAT = '{time:YYYY-MM-DD HH:mm:ss}  | {level} > {elapsed}  | {message}'  # 每条日志输出格式

LOG_DIR = "./log/"  # os.path.dirname(os.getcwd())  # 日志文件路径
LOG_LEVEL = 'DEBUG'  # 日志级别


def get_logger(name=None):
    global loggers_container
    if not name:
        name = __name__
    if loggers_container.get(name):
        return loggers_container.get(name)

    # 输出到文件配置
    if LOG_ENABLED and LOG_TO_CONSOLE:
        pass
        # logger.remove(handler_id=None)
        # logger.add(sys.stderr, format=LOG_FORMAT, level=LOG_LEVEL)

    # 输出到文件配置
    if LOG_ENABLED and LOG_TO_FILE:
        log_dir = os.path.dirname(LOG_DIR)
        # log_file = datetime.datetime.now().strftime('%Y-%m-%d') + ".log"
        log_file = "news_rmt.log"
        log_path = os.path.join(log_dir, log_file)
        logger.add(log_path,
                   encoding='utf-8',
                   rotation='1 days',
                   retention='20 days',  # 设置历史保留时长
                   backtrace=True,  # 回溯
                   diagnose=True,  # 诊断
                   enqueue=True  # 异步写
                   )
    loggers_container[name] = logger
    return logger
