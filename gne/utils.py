import os
import re
import yaml
from lxml.html import fromstring, HtmlElement
from lxml.html import etree
from urllib.parse import urlparse, urljoin
from .defaults import USELESS_TAG, TAGS_CAN_BE_REMOVE_IF_EMPTY, USELESS_ATTR, HIGH_WEIGHT_ARRT_KEYWORD


def normalize_node(element: HtmlElement):
    etree.strip_elements(element, *USELESS_TAG)
    for node in iter_node(element):
        # inspired by readability.
        if node.tag.lower() in TAGS_CAN_BE_REMOVE_IF_EMPTY and is_empty_element(node):
            remove_node(node)

        # merge text in span or strong to parent p tag
        if node.tag.lower() == 'p':
            etree.strip_tags(node, 'span')
            etree.strip_tags(node, 'strong')

        # if a div tag does not contain any sub node, it could be converted to p node.
        if node.tag.lower() == 'div' and not node.getchildren():
            node.tag = 'p'

        if node.tag.lower() == 'span' and not node.getchildren():
            node.tag = 'p'

        # remove empty p tag
        if node.tag.lower() == 'p' and not node.xpath('.//img'):
            if not (node.text and node.text.strip()):
                drop_tag(node)

        class_name = node.get('class')
        if class_name:
            if class_name in USELESS_ATTR:
                remove_node(node)
                break


def html2element(html):
    html = re.sub('</?br.*?>', '', html)
    element = fromstring(html)
    return element


def pre_parse(element):
    normalize_node(element)

    return element


def remove_noise_node(element, noise_xpath_list):
    noise_xpath_list = noise_xpath_list or config.get('noise_node_list')
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
    if parent is not None:
        parent.remove(node)


def drop_tag(node: HtmlElement):
    """
    only delete the tag, but merge its text to parent.
    :param node:
    :return:
    """
    parent = node.getparent()
    if parent is not None:
        node.drop_tag()


def is_empty_element(node: HtmlElement):
    return not node.getchildren() and not node.text


def pad_host_for_images(host, url):
    """
    网站上的图片可能有如下几种格式：

    完整的绝对路径：https://xxx.com/1.jpg
    完全不含 host 的相对路径： /1.jpg
    含 host 但是不含 scheme:  xxx.com/1.jpg 或者  ://xxx.com/1.jpg

    :param host:
    :param url:
    :return:
    """
    if url.startswith('http'):
        return url
    parsed_uri = urlparse(host)
    scheme = parsed_uri.scheme
    if url.startswith(':'):
        return f'{scheme}{url}'
    if url.startswith('//'):
        return f'{scheme}:{url}'
    return urljoin(host, url)


def read_config():
    if os.path.exists('.gne'):
        with open('.gne', encoding='utf-8') as f:
            config_text = f.read()
        config = yaml.safe_load(config_text)
        return config
    return {}


def get_high_weight_keyword_pattern():
    return re.compile('|'.join(HIGH_WEIGHT_ARRT_KEYWORD), flags=re.I)


def get_longest_common_sub_string(str1: str, str2: str) -> str:
    """
    获取两个字符串的最长公共子串。

    构造一个矩阵，横向是字符串1，纵向是字符串2，例如：

      青南是天才！？
    听0 0 0 0 00 0
    说0 0 0 0 00 0
    青1 0 0 0 00 0
    南0 1 0 0 00 0
    是0 0 1 0 00 0
    天0 0 0 1 00 0
    才0 0 0 0 10 0
    ！0 0 0 0 01 0

    显然，只要斜对角线最长的就是最长公共子串

    :param str1:
    :param str2:
    :return:
    """
    if not all([str1, str2]):
        return ''
    matrix = [[0] * (len(str2) + 1) for _ in range(len(str1) + 1)]
    max_length = 0
    start_position = 0
    for index_of_str1 in range(1, len(str1) + 1):
        for index_of_str2 in range(1, len(str2) + 1):
            if str1[index_of_str1 - 1] == str2[index_of_str2 - 1]:
                matrix[index_of_str1][index_of_str2] = matrix[index_of_str1 - 1][index_of_str2 - 1] + 1
                if matrix[index_of_str1][index_of_str2] > max_length:
                    max_length = matrix[index_of_str1][index_of_str2]
                    start_position = index_of_str1 - max_length
            else:
                matrix[index_of_str1][index_of_str2] = 0
    return str1[start_position: start_position + max_length]


config = read_config()
