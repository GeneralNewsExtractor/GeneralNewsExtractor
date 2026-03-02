import re
from gne.utils import config
from lxml.html import HtmlElement
from gne.defaults import AUTHOR_PATTERN


class AuthorExtractor:
    def __init__(self):
        self.author_pattern = AUTHOR_PATTERN

    @staticmethod
    def _is_valid_author(text):
        """检查 meta author 内容是否是有效的作者名"""
        if not text:
            return False
        # 纯数字不是作者名
        if text.isdigit():
            return False
        # 含 @ 号的是邮箱
        if '@' in text:
            return False
        # 常见占位符
        if text.lower() in ('name', 'author', 'admin', 'editor', 'test'):
            return False
        # 太长或太短
        if len(text) < 2 or len(text) > 30:
            return False
        return True

    def extractor(self, element: HtmlElement, author_xpath=''):
        author_xpath = author_xpath or config.get('author', {}).get('xpath')
        if author_xpath:
            author = ''.join(element.xpath(author_xpath))
            return author
        # 优先从 meta 标签提取作者
        meta_author = element.xpath('//meta[@name="author"]/@content')
        if meta_author:
            author = meta_author[0].strip()
            if self._is_valid_author(author):
                return author
        text = ''.join(element.xpath('.//text()'))
        for pattern in self.author_pattern:
            author_obj = pattern.search(text)
            if author_obj:
                return author_obj.group(1)
        return ''
