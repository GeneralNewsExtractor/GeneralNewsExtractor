import re
from lxml.html import HtmlElement
from gne.defaults import DATETIME_PATTERN


class TimeExtractor:
    def __init__(self):
        self.time_pattern = DATETIME_PATTERN

    def extractor(self, element: HtmlElement):
        text = ''.join(element.xpath('.//text()'))
        for dt in self.time_pattern:
            dt_obj = re.search(dt, text)
            if dt_obj:
                return dt_obj.group(1)
        else:
            return ''
