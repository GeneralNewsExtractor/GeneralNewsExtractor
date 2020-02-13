import re
from gne.utils import config
from lxml.html import HtmlElement
from gne.defaults import AUTHOR_PATTERN


class AuthorExtractor:
    def __init__(self):
        self.author_pattern = AUTHOR_PATTERN

    def extractor(self, element: HtmlElement, author_xpath=''):
        author_xpath = author_xpath or config.get('author', {}).get('xpath')
        if author_xpath:
            author = ''.join(element.xpath(author_xpath))
            return author
        text = ''.join(element.xpath('.//text()'))
        for pattern in self.author_pattern:
            author_obj = re.search(pattern, text)
            if author_obj:
                return author_obj.group(1)
        return ''
