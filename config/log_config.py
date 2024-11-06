import os
import logging
from logging.handlers import RotatingFileHandler


class LogConfig:
    # 日志级别
    LOG_LEVEL = logging.INFO

    # 日志格式
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # 日志文件路径
    LOG_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "log"
    )

    # 确保日志目录存在
    os.makedirs(LOG_PATH, exist_ok=True)

    # 日志文件名
    LOG_FILE = os.path.join(LOG_PATH, "app.log")

    # 单个日志文件的最大大小（5MB）
    MAX_LOG_SIZE = 5 * 1024 * 1024

    # 保留的日志文件数量
    BACKUP_COUNT = 5

    @classmethod
    def get_logger(cls, name):
        logger = logging.getLogger(name)
        logger.setLevel(cls.LOG_LEVEL)

        # 创建 RotatingFileHandler
        file_handler = RotatingFileHandler(
            cls.LOG_FILE, maxBytes=cls.MAX_LOG_SIZE, backupCount=cls.BACKUP_COUNT
        )
        file_handler.setLevel(cls.LOG_LEVEL)

        # 创建 Formatter
        formatter = logging.Formatter(cls.LOG_FORMAT)
        file_handler.setFormatter(formatter)

        # 添加 Handler 到 Logger
        logger.addHandler(file_handler)

        return logger
