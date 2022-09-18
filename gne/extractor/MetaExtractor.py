from lxml.html import HtmlElement
from typing import List, Dict


class MetaExtractor:
    def extract_meta(self, name_attribute: str, content_attribute: str = 'content') -> Dict[str, str]:
        """

        :param name_attribute: 名称对应的属性名，例如<meta name="xxx">是name，<meta property="xxx">是property
        :param content_attribute: 内容对应的属性名，一般是content
        :return:
        """

    def extract(self, element: HtmlElement) -> Dict[str, str]:
        meta_list = element.xpath('//meta')
        meta_content = {}
        for meta in meta_list:
            name = meta.xpath('@name|@property')
            if not name:
                continue
            content = meta.xpath('@content')
            if not content:
                continue
            meta_content[name[0]] = content[0]
        return meta_content
