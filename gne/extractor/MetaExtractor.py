from lxml.html import HtmlElement
from typing import Dict


class MetaExtractor:
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
