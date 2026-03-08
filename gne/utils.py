import os
import re
import yaml
import unicodedata
from lxml.html import fromstring, HtmlElement
from lxml.html import etree
from urllib.parse import urlparse, urljoin
from .defaults import USELESS_TAG, TAGS_CAN_BE_REMOVE_IF_EMPTY, USELESS_ATTR, HIGH_WEIGHT_ARRT_KEYWORD

_BR_RE = re.compile(r'</?br.*?>')
HIGH_WEIGHT_KEYWORD_RE = re.compile('|'.join(HIGH_WEIGHT_ARRT_KEYWORD), flags=re.I)


def _is_useless_node(class_name, id_name):
    """检查节点的 class 或 id 是否表明它是噪声节点。
    使用按分隔符拆分后的词级匹配，避免短关键词（如 'ad'、'nav'）的子串误匹配。
    """
    for value in (class_name, id_name):
        if not value:
            continue
        value_lower = value.lower()
        # 先按空格拆分出各个 class/id，再按 - 和 _ 拆分为词
        for cls in value_lower.split():
            if cls in USELESS_ATTR:
                return True
            parts = re.split(r'[-_]+', cls)
            if any(part in USELESS_ATTR for part in parts):
                return True
    return False


def normalize_node(element: HtmlElement):
    etree.strip_elements(element, *USELESS_TAG)
    # 先收集需要删除的节点，避免遍历过程中修改树结构
    nodes_to_remove = []
    for node in list(iter_node(element)):
        # inspired by readability.
        if node.tag.lower() in TAGS_CAN_BE_REMOVE_IF_EMPTY and is_empty_element(node):
            remove_node(node)
            continue

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
                continue

        class_name = node.get('class', '')
        id_name = node.get('id', '')
        if class_name or id_name:
            if node.tag.lower() not in ('body', 'html') and _is_useless_node(class_name, id_name):
                nodes_to_remove.append(node)

    for node in nodes_to_remove:
        remove_node(node)


def html2element(html):
    html = _BR_RE.sub('', html)
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
    return HIGH_WEIGHT_KEYWORD_RE


def get_longest_common_sub_string(str1: str, str2: str) -> str:
    """
    获取两个字符串的最长公共子串。使用滚动数组优化空间复杂度为 O(min(n,m))。

    :param str1:
    :param str2:
    :return:
    """
    if not all([str1, str2]):
        return ''
    # 确保 str2 是较短的字符串，以优化空间
    if len(str1) < len(str2):
        str1, str2 = str2, str1
    prev_row = [0] * (len(str2) + 1)
    max_length = 0
    start_position = 0
    for index_of_str1 in range(1, len(str1) + 1):
        curr_row = [0] * (len(str2) + 1)
        for index_of_str2 in range(1, len(str2) + 1):
            if str1[index_of_str1 - 1] == str2[index_of_str2 - 1]:
                curr_row[index_of_str2] = prev_row[index_of_str2 - 1] + 1
                if curr_row[index_of_str2] > max_length:
                    max_length = curr_row[index_of_str2]
                    start_position = index_of_str1 - max_length
        prev_row = curr_row
    return str1[start_position: start_position + max_length]


def normalize_text(html):
    """
    使用 NFKC 对网页源代码进行归一化，把特殊符号转换为普通符号
    注意，中文标点符号可能会被转换成英文标点符合。
    :param html:
    :return:
    """
    return unicodedata.normalize('NFKC', html)


def fix_html(html):
    """
    有一些网站的HTML不规范，比如</html>出现在源代码的中间。这个时候需要修复一下。
    :param html:
    :return: html
    """
    new_html = html.replace('</html>', '')
    new_html = f'{new_html}</html>'
    return new_html


config = read_config()
