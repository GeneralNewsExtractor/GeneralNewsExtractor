import re
from lxml.html import HtmlElement


class AuthorExtractor:
    def __init__(self):
        self.author_pattern = [
            "责编[：|:| |丨|/]\s*([\u4E00-\u9FA5]{2,5})[^\u4E00-\u9FA5|:|：]",
            "作者[：|:| |丨|/]\s*([\u4E00-\u9FA5]{2,5})[^\u4E00-\u9FA5|:|：]",
            "编辑[：|:| |丨|/]\s*([\u4E00-\u9FA5]{2,5})[^\u4E00-\u9FA5|:|：]",
            "文[：|:| |丨|/]\s*([\u4E00-\u9FA5]{2,5})[^\u4E00-\u9FA5|:|：]",
            "撰文[：|:| |丨|/]\s*([\u4E00-\u9FA5]{2,5})[^\u4E00-\u9FA5|:|：]"
        ]

    def extractor(self, element: HtmlElement):
        text = ''.join(element.xpath('.//text()'))
        for pattern in self.author_pattern:
            author_obj = re.search(pattern, text)
            if author_obj:
                return author_obj.group(1)
        return ''
