import os.path
import yaml

from common.logger import logger


def load_yaml_config(file_path: str = None) -> dict:
    """
    加载yaml文件
    :param file_path: 配置文件绝对路径
    :return: 字典格式数据：key/value
    """
    try:
        if file_path is None:
            # 默认读取配置文件config.yaml
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(project_root, "config", "config.yaml")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"找不到指定文件：{file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
            logger.info(f"读取文件{file}成功")
            if not isinstance(config, dict):
                raise TypeError(f"config 类型错误，应传入字典，实传入：{type(config).__name__}")
            return config
    except Exception as e:
        logger.error(f"读取文件{file}失败，异常信息：{e}")
        return {}
