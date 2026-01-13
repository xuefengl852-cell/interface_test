import ast
import json

import allure
import pytest

from common.excel_reader_util import ExcelReaderUtil
from common.logger import logger
from common.request_handler import send_request

login_data = ExcelReaderUtil.read_excel("../data/tmall_interface_test.xlsx",sheet_name="Sheet1")


def parse_params(param_str):
    """安全解析参数字符串为字典"""
    if not param_str or not param_str.strip():
        return None
    try:
        # 处理换行符/空格，避免解析错误
        clean_str = param_str.replace("\n", "").replace(" ", "")
        return ast.literal_eval(clean_str)
    except (SyntaxError, ValueError) as e:
        logger.error(f"参数解析失败：{param_str}，错误：{e}")
        return None
    
@allure.story("接口测试")
class TestLogin:
    @allure.title("登录接口")
    @pytest.mark.parametrize("login_interface_data",login_data)
    def test_login(self, login_interface_data):
        with allure.step("请求接口"):
            form_params = parse_params(login_interface_data['URL参数'])
            response = send_request(
                method=login_interface_data['请求方式'],
                url=login_interface_data['接口URL'],
                data=form_params
            )

            logger.info(f"URL参数：{form_params}")
            logger.info(f"{response}")
        with allure.step("断言返回值是否正确"):
            expected_status_code = login_interface_data['预期状态码']
            logger.info(f"""
            ========== 完整响应信息 ==========
            状态码: {response.status_code}
            响应URL: {response.url}
            耗时: {response.elapsed.total_seconds():.3f}s
            响应头: {dict(response.headers)}
            Cookie: {dict(response.cookies)}
            响应体: {json.dumps(response.json(), ensure_ascii=False, indent=2) if response.headers.get('Content-Type', '').startswith('application/json') else response.text}
            =================================
            """)
            assert response.status_code == expected_status_code, \
                f"HTTP状态码断言失败！预期{expected_status_code}，实际{response.status_code}"
