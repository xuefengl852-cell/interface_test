import logging
import os
from datetime import datetime
from colorlog import ColoredFormatter

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


def setup_logger(
      name: str = "api_auto_test",
      console_level: str = "INFO",
      file_level: str = "DEBUG"
) -> logging.Logger:
    """
    配置日志器：控制台输出INFO，文件输出DEBUG，每次运行生成新的时间戳日志文件
    :param name: 日志器名称
    :param console_level: 控制台日志级别
    :param file_level: 文件日志级别
    :return: 配置好的Logger实例
    """
    # 1. 创建日志器并设置全局最低级别（必须低于两个handler的级别）
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 全局最低级别为DEBUG
    logger.handlers.clear()  # 避免重复添加处理器
    
    # 2. 定义日志格式
    basic_format = "%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s"
    color_format = "%(log_color)s%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s%(reset)s"
    
    # 3. 控制台处理器（输出INFO及以上）
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_formatter = ColoredFormatter(
        color_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    console_handler.setFormatter(console_formatter)
    
    # 4. 文件处理器（输出DEBUG及以上，每次运行生成新文件）
    # 生成带时间戳的日志文件名（精确到毫秒，避免重复）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # 保留到毫秒
    log_file_name = f"api_test_{timestamp}.log"
    log_file_path = os.path.join(LOG_DIR, log_file_name)
    
    file_handler = logging.FileHandler(
        filename=log_file_path,
        mode="a",
        encoding="utf-8"
    )
    file_handler.setLevel(file_level)
    file_formatter = logging.Formatter(basic_format, datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(file_formatter)
    
    # 5. 添加处理器到日志器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


# 创建全局日志实例
logger = setup_logger()


