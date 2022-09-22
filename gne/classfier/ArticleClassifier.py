from lxml.html import Element
from gne.defaults import ARTICLE_XPATH
from gne.utils import iter_node


class ArticleClassifier:
    def __init__(self, element: Element):
        self.element = element

    def classify(self):
        for xpath in ARTICLE_XPATH:
            if self.element.xpath(xpath):
                return True
        return self.classfy_by_weight()

    def classify_by_weight(self):
        has_title = False
        if self.element.xpath('//h1 || //h2 || //header'):
            has_title = True
        body = self.element.xpath('//body')
        if not body:
            body = self.element
        else:
            body = body[0]
        for node in iter_node(body):
            class_ = node.attrib.get('class', '').lower()
            tag = node.tag.lower()
            if tag in ['h3', 'h4', 'p', 'div']:
                if (
                    'title' in class_
                    or 'header' in class_
                    or 'headline' in class_
                ):
                    has_title = True
                    break
