import re
from gne.utils import config
from collections import deque
from lxml.html import HtmlElement


class ListExtractor:
    def extract(self, element: HtmlElement, feature):
        result = []
        if feature.startswith('/'):
            feature_element = element.xpath(feature)
        else:
            feature_element = element.xpath(f'//*[contains(text(), "{feature}")]')

        if not feature_element:
            print('找不到 feature！')
            return result

        parent = feature_element[0]
        leaf_class = parent.attrib.get('class', '')
        if leaf_class:
            leaf_node = f'{parent.tag}[@class="{leaf_class}"]'
        else:
            leaf_node = parent.tag
        is_a_tag = parent.tag == 'a'
        sub_path_queue = deque([leaf_node])
        while parent is not None:
            parent = parent.getparent()
            if parent is None:
                break
            path = '/'.join(sub_path_queue)
            item_list = parent.xpath(path)
            if len(item_list) > 3:
                for item in item_list:
                    item_info = {'title': ''.join(item.xpath('text()'))}
                    if is_a_tag:
                        item_info['url'] = ''.join(item.xpath('@href'))
                    result.append(item_info)
                return result
            sub_path_queue.insert(0, parent.tag)
        return result


