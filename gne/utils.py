from .defaults import USELESS_TAG
from lxml.html import fromstring, HtmlElement


def normalize_node(element: HtmlElement):
    for node in iter_node(element):
        if node.tag.lower() in USELESS_TAG:
            remove_node(node)
        if node.tag.lower() == 'span' and not node.getchildren() and not node.text:
            remove_node(node)

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
    node.getparent().remove(node)
