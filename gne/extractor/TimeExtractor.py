import re
from gne.utils import config
from lxml.html import HtmlElement
from gne.defaults import DATETIME_PATTERN, PUBLISH_TIME_META

_DATE_SEP_RE = re.compile(r'[-/.]')


class TimeExtractor:
    def __init__(self):
        self.time_pattern = DATETIME_PATTERN

    def extractor(self, element: HtmlElement, publish_time_xpath: str = '') -> str:
        publish_time_xpath = publish_time_xpath or config.get('publish_time', {}).get('xpath')
        publish_time = (self.extract_from_user_xpath(publish_time_xpath, element)  # 用户指定的 Xpath 是第一优先级
                        or self.extract_from_meta(element)   # 第二优先级从 Meta 中提取
                        or self.extract_from_text(element))  # 最坏的情况从正文中提取
        return publish_time

    def extract_from_user_xpath(self, publish_time_xpath: str, element: HtmlElement) -> str:
        if publish_time_xpath:
            publish_time = ''.join(element.xpath(publish_time_xpath))
            return publish_time
        return ''

    @staticmethod
    def _is_valid_date(date_str):
        """基本日期校验：月份 1-12，日 1-31"""
        # 提取日期部分（去掉时间部分）
        date_part = date_str.strip().split()[0]
        # 替换中文年月日为分隔符
        date_part = date_part.replace('年', '-').replace('月', '-').replace('日', '')
        parts = _DATE_SEP_RE.split(date_part)
        try:
            if len(parts) >= 3:
                month = int(parts[-2])
                day = int(parts[-1])
                if month < 1 or month > 12:
                    return False
                if day < 1 or day > 31:
                    return False
        except (ValueError, IndexError):
            pass
        return True

    def extract_from_text(self, element: HtmlElement) -> str:
        text = ''.join(element.xpath('.//text()'))
        for dt in self.time_pattern:
            dt_obj = dt.search(text)
            if dt_obj:
                result = dt_obj.group(1)
                if self._is_valid_date(result):
                    return result
        return ''

    def extract_from_meta(self, element: HtmlElement) -> str:
        """
        一些很规范的新闻网站，会把新闻的发布时间放在 META 中，因此应该优先检查 META 数据
        :param element: 网页源代码对应的Dom 树
        :return: str
        """
        for xpath in PUBLISH_TIME_META:
            publish_time = element.xpath(xpath)
            if publish_time:
                return ''.join(publish_time)
        return ''
