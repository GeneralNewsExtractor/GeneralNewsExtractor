from .defaults import USELESS_TAG, TAGS_CAN_BE_REMOVE_IF_EMPTY
from lxml.html import fromstring, HtmlElement
from lxml.html import etree


def normalize_node(element: HtmlElement):
    for node in iter_node(element):
        if node.tag.lower() in USELESS_TAG:
            remove_node(node)

        # inspired by readability.
        if node.tag.lower() in TAGS_CAN_BE_REMOVE_IF_EMPTY and is_empty_element(node):
            remove_node(node)

        # p 标签下面的 span 标签中的文字，可以合并到 p 标签中
        if node.tag.lower() == 'p':
            etree.strip_tags(node, 'span')

        # if a div tag does not contain any sub node, it could be converted to p node.
        if node.tag.lower() == 'div' and not node.getchildren():
            node.tag = 'p'

        class_name = node.get('class')
        if class_name and ('share' in class_name or 'contribution' in class_name):
            remove_node(node)


def pre_parse(html):
    element = fromstring(html)
    normalize_node(element)
    return element


def remove_noise_node(element, noise_xpath_list):
    if not noise_xpath_list:
        return
    for noise_xpath in noise_xpath_list:
        nodes = element.xpath(noise_xpath)
        for node in nodes:
            remove_node(node)
    return element


def iter_node(element: HtmlElement):
    yield element
    for sub_element in element:
        if isinstance(sub_element, HtmlElement):
            yield from iter_node(sub_element)


def remove_node(node: HtmlElement):
    """
    this is a in-place operation, not necessary to return
    :param node:
    :return:
    """
    parent = node.getparent()
    if parent:
        parent.remove(node)


def is_empty_element(node: HtmlElement):
    return not node.getchildren() and not node.text
