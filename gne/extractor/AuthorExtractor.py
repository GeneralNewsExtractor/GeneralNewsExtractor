import re
import json
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

    def extract_from_json_ld(self, element: HtmlElement) -> str:
        scripts = element.xpath('//script[@type="application/ld+json"]/text()')
        for script_text in scripts:
            try:
                data = json.loads(script_text.strip())
                if isinstance(data, list):
                    data = data[0]
                if not isinstance(data, dict):
                    continue
                author = data.get('author')
                if not author:
                    continue
                if isinstance(author, str):
                    if self._is_valid_author(author):
                        return author
                elif isinstance(author, dict):
                    name = author.get('name', '')
                    if self._is_valid_author(name):
                        return name
                elif isinstance(author, list) and author:
                    first = author[0]
                    name = first.get('name', '') if isinstance(first, dict) else str(first)
                    if self._is_valid_author(name):
                        return name
            except (json.JSONDecodeError, IndexError, TypeError):
                continue
        return ''

    def extractor(self, element: HtmlElement, author_xpath=''):
        author_xpath = author_xpath or config.get('author', {}).get('xpath')
        if author_xpath:
            author = ''.join(element.xpath(author_xpath))
            return author
        # 优先从 JSON-LD 结构化数据提取作者
        json_ld_author = self.extract_from_json_ld(element)
        if json_ld_author:
            return json_ld_author
        # 从 meta 标签提取作者
        meta_author = element.xpath('//meta[@name="author"]/@content')
        if meta_author:
            author = meta_author[0].strip()
            if self._is_valid_author(author):
                return author
        # 从 itemprop="author" 提取
        itemprop_author = element.xpath('//*[@itemprop="author"]//text()')
        if itemprop_author:
            author = ''.join(itemprop_author).strip()
            if self._is_valid_author(author):
                return author
        # 从 class/rel="author" 的标签提取
        class_author = element.xpath('//*[@class="author"]//text() | //a[@rel="author"]//text()')
        if class_author:
            author = ''.join(class_author).strip()
            if self._is_valid_author(author):
                return author
        # 最后从全文正则匹配
        text = ''.join(element.xpath('.//text()'))
        for pattern in self.author_pattern:
            author_obj = pattern.search(text)
            if author_obj:
                return author_obj.group(1)
        return ''
