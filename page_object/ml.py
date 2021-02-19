# author:丑牛
# datetime:2021/1/14 15:50
from selenium.common.exceptions import NoSuchElementException

from common.readelement import Element
from page.webpage import WebPage
from utils.logger import log
from utils.times import sleep

home = Element('ml')


class Page(WebPage):
    """主页类"""

    def click_ele(self, group, label_name):
        """点击侧边栏,打开标签页"""
        self.is_click(home.__getitem__(group, label_name))

    def get_ele_text(self, group, label_name):
        """获取标签页element的文本值"""
        label_text = self.element_text(home.__getitem__(group, label_name))
        return label_text

    def input_ele(self, group, label_name, txt):
        """输入文字"""
        self.input_text(home.__getitem__(group, label_name), txt)
        sleep(1)

    def ele_input_file(self, group, label_name, txt):
        """上传文件"""
        self.input_file(home.__getitem__(group, label_name), txt)
        sleep(2)

    def exist_ele(self, group, label_name):
        """判断元素是否存在"""
        try:
            self.find_element(home.__getitem__(group, label_name))
            return True
        except NoSuchElementException as e:
            log.error(e)
            return False

    def enable_ele(self, group, label_name):
        """判断页面元素是够可操作"""
        return self.is_active(home.__getitem__(group, label_name))

    def clear_ele(self, group, label_name):
        """输入框值清空"""
        return self.is_clear(home.__getitem__(group, label_name))

    def is_exist(self, group, label_name):
        """获取多个相同element的文本值，并对值进行判断"""
        ele_list = self.find_elements(home.__getitem__(group, label_name))
        i = 0
        for ele in ele_list[0:5]:
            text = ele.text
            if '必须' in text:
                log.info(text)
                i = i + 1
        log.info(ele_list[5].text)
        if 'json' in ele_list[5].text:
            i = i + 1
        if i == 6:
            return True
        else:
            return False

    def click_next(self, group, label_name):
        """获取两个及以上的element，然后操作第二个element"""
        ele_list = self.find_elements(home.__getitem__(group, label_name))
        ele_list[1].click()
        sleep(2)

    def get_search_table_result(self, group, label_name):
        ele = self.find_tr(home.__getitem__(group, label_name))
        num = len(ele)
        if num == 0:
            text = self.element_text(home.__getitem__('算法', '无数据'))
            return text
        return num

    @property
    def imagine(self):
        """获取所有的实验名"""
        return [x.text for x in self.find_elements(home.__getitem__('实验', '实验名'))]

    def quit_webdriver(self):
        """获取所有的实验名"""
        self.quit()