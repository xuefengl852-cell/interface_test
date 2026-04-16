import logging
from unittest import TestCase

import allure
import pytest

from common.excel_reader_util import ExcelReaderUtil
from common.request_handler import send_request
from common.yaml_loader import load_yaml_config
loona_router = ExcelReaderUtil.read_excel("../data/test_data_case/agent_router_415_cases.xlsx")
column_list_router = [item["真实请求体"] for item in loona_router]


allure.epic("agent测试-loona")
@pytest.mark.parametrize(
    "router_request_body",column_list_router
)
class TestCaseOne():

    def test_case_one(self, router_request_body):
        with allure.step(""):
            logging.info(f"当前的请求体内容为：{router_request_body}")