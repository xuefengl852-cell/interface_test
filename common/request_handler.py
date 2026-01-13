import requests

from common.logger import logger
from common.yaml_loader import load_yaml_config

config_yaml = load_yaml_config()


def send_request(method, url, **kwargs):
    try:
        """请求接口通用方法"""
        interface = config_yaml['base_url'] + url
        response = requests.request(
            method=method,
            url=interface,
            timeout=config_yaml['timeout'],
            **kwargs
        )
        logger.info(f"请求地址为：{interface}，请求方式为：{method}")
        return response
    except Exception as e:
        raise RuntimeError(f"请求失败：{str(e)}")
