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
        # 优先从 meta 标签提取作者
        meta_author = element.xpath('//meta[@name="author"]/@content')
        if meta_author and meta_author[0].strip():
            return meta_author[0].strip()
        text = ''.join(element.xpath('.//text()'))
        for pattern in self.author_pattern:
            author_obj = pattern.search(text)
            if author_obj:
                return author_obj.group(1)
        return ''
