# author:丑牛
# datetime:2021/1/14 16:43
import re
import pytest
from common.readconfig import ini
from page_object.ml import Page
from utils.logger import log
from utils.times import sleep


class TestMl:
    @pytest.fixture(scope='function', autouse=True)
    def open(self, drivers):
        """打开机器学习平台"""
        page = Page(drivers)
        page.get_url(ini.url)

    def test_001(self, drivers):
        """test_001 测试实验页面"""
        # 打开实验管理页面
        page = Page(drivers)
        page.input_ele('登录', '用户名', 'wangzhaoxian')
        page.input_ele('登录', '密码', '123456')
        page.click_ele('登录', '登录')
        page.click_ele('侧边栏', '实验')
        text = page.get_ele_text('通用', '页面名称')
        result = re.search('实验列表', text)
        log.info(result)
        assert result
        # 测试新增页面取消按键
        page.click_ele('实验', '新增实验')
        text = page.get_ele_text('通用', '对话页面')
        result = re.search('实验信息', text)
        log.info(result)
        assert result
        page.click_ele('通用', '取消')
        # 表单校验
        page.click_ele('实验', '新增实验')
        page.click_ele('通用', '确定')
        text = page.get_ele_text('通用', '错误信息')
        result = re.search('必须', text)
        log.info(result)
        assert result
        # 测试实验页面新增实验
        page.input_ele('实验', '实验命名', 'Ctest')
        page.input_ele('实验', '模型描述', '测试')
        page.click_ele('通用', '确定')
        page.click_ele('翻页', '第4页')
        result = page.exist_ele('实验', '测试')
        assert result
        # 测试实验页面修改-取消
        page.click_ele('翻页', '第4页')
        page.click_ele('实验', '测试')
        page.click_ele('通用', '取消')
        # 测试实验页面修改-编辑
        page.click_ele('翻页', '第4页')
        page.click_ele('实验', '测试')
        result = page.enable_ele('实验', '实验命名')
        assert result is False
        result = page.enable_ele('实验', '模型描述')
        assert result is False
        # 修改
        page.click_ele('实验', '编辑')
        page.input_ele('实验', '实验命名', 'testupdate')
        page.input_ele('实验', '模型描述', '测试修改')
        page.click_ele('通用', '确定')
        page.click_ele('翻页', '第4页')
        result = page.exist_ele('实验', '修改后')
        assert result
        # 测试打开
        page.click_ele('翻页', '第4页')
        page.click_ele('实验', '实验打开')
        page.click_ele('关闭', '编排')
        # 测试删除-取消
        sleep(1)
        page.click_ele('翻页', '第4页')
        page.click_ele('实验', '删除')
        page.click_ele('通用', '撤销')
        result = page.exist_ele('实验', '修改后')
        assert result
        # 测试删除-确认
        page.click_ele('实验', '删除')
        page.click_ele('通用', '确认')
        sleep(1)
        page.click_ele('翻页', '第4页')
        result_text = page.imagine
        log.info("实验名称：{}".format(result_text))
        if "testupdate" in result_text:
            result = False
        else:
            result = True
        assert result

    def test_002(self, drivers):
        """test_002 测试算法页面"""
        # 打开算法管理页面
        page = Page(drivers)
        page.click_ele('侧边栏', '算法')
        sleep(2)
        text = page.get_ele_text('通用', '页面名称')
        result = re.search('算法管理', text)
        log.info(result)
        assert result
        # 新建算法-取消
        page.click_ele('算法', '新建')
        page.input_ele('算法', '规格参数', 'test')
        page.click_ele('通用', '确定')
        result = page.is_exist('通用', '错误信息')
        assert result
        page.click_ele('通用', '取消')
        # 表单校验
        page.click_ele('算法', '新建')
        text = page.get_ele_text('通用', '对话页面')
        result = re.search('算法信息', text)
        log.info(result)
        assert result
        page.input_ele('算法', '算法标识', 'zmjtest')
        page.input_ele('算法', '算法名称', 'zmjtest')
        page.click_ele('算法', '算法框架')
        page.click_ele('算法', 'tensorflow')
        page.click_ele('算法', '算法分类')
        page.click_next('算法', '机器学习算法')
        page.click_ele('算法', '模型评估')
        page.ele_input_file('算法', '算法包', 'C:\\Users\\wangzhaoxian\\Downloads\\1.csv')
        page.input_ele('算法', '算法主类', 'zmjtest')
        page.input_ele('算法', '规格参数', '[]')
        page.input_ele('算法', '算法描述', 'zmjtest')
        page.click_ele('通用', '确定')
        # 查询-重置
        page.input_ele('算法', '查询算法名称', 'zmjtest')
        page.click_ele('算法', '重置')
        text = page.get_ele_text('算法', '查询算法名称')
        log.info(text)
        result = len(text) == 0
        assert result
        # 查询-无结果
        page.input_ele('算法', '查询算法名称', '1')
        page.click_ele('算法', '所属分类')
        page.click_ele('算法', '机器学习算法')
        page.click_ele('算法', '模型评估')
        page.click_ele('算法', '查询')
        sleep(3)
        text = page.get_search_table_result('算法', '结果表')
        result = re.search('暂无数据', text)
        assert result
        # 查询-有结果-编辑
        page.input_ele('算法', '查询算法名称', 'zmjtest')
        page.click_ele('算法', '所属分类')
        page.click_ele('算法', '机器学习算法')
        page.click_ele('算法', '模型评估')
        page.click_ele('算法', '查询')
        sleep(3)
        text = page.get_search_table_result('算法', '结果表')
        assert text == 1
        page.click_ele('算法', '编辑')
        page.click_ele('通用', '取消')
        page.click_ele('算法', '编辑')
        page.input_ele('算法', '算法标识', 'zmjtestupdate')
        page.click_ele('通用', '确定')
        # 删除
        page.click_ele('算法', '查询')
        sleep(3)
        page.click_ele('通用', '删除')
        page.click_ele('通用', '撤销')
        page.click_ele('通用', '删除')
        page.click_ele('通用', '确认')
        page.click_ele('算法', '查询')
        text = page.get_search_table_result('算法', '结果表')
        result = re.search('暂无数据', text)
        assert result

    # def test_003(self, drivers):
    #     """test_003 测试数据页面"""
    #     # 打开数据管理页面
    #     page = Page(drivers)
    #     page.click_ele('侧边栏', '数据')
    #     text = page.get_ele_text('通用', '页面名称')
    #     result = re.search('数据管理', text)
    #     log.info(result)
    #     assert result


if __name__ == '__main__':
    pytest.main(['TestCase/test_ml.py'])
