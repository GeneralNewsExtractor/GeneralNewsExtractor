import re
import numpy as np
from lxml.html import etree
from html import unescape
from gne.utils import iter_node, pad_host_for_images, config, get_high_weight_keyword_pattern


class ContentExtractor:
    def __init__(self, content_tag='p'):
        """

        :param content_tag: 正文内容在哪个标签里面
        """
        self.content_tag = content_tag
        self.node_info = {}
        self.high_weight_keyword_pattern = get_high_weight_keyword_pattern()
        self.punctuation = set('''！，。？、；：“”‘’《》%（）,.?:;'"!%()''')  # 常见的中英文标点符号
        self.element_text_cache = {}

    def extract(self, selector, host='', body_xpath='', with_body_html=False):
        body_xpath = body_xpath or config.get('body', {}).get('xpath', '')
        if body_xpath:
            body = selector.xpath(body_xpath)[0]
        else:
            body = selector.xpath('//body')[0]
        for node in iter_node(body):
            node_hash = hash(node)
            density_info = self.calc_text_density(node)
            text_density = density_info['density']
            ti_text = density_info['ti_text']
            text_tag_count = self.count_text_tag(node, tag='p')
            sbdi = self.calc_sbdi(ti_text, density_info['ti'], density_info['lti'])
            images_list = node.xpath('.//img/@src')
            host = host or config.get('host', '')
            if host:
                images_list = [pad_host_for_images(host, url) for url in images_list]
            node_info = {'ti': density_info['ti'],
                         'lti': density_info['lti'],
                         'tgi': density_info['tgi'],
                         'ltgi': density_info['ltgi'],
                         'node': node,
                         'density': text_density,
                         'text': ti_text,
                         'images': images_list,
                         'text_tag_count': text_tag_count,
                         'sbdi': sbdi}
            if with_body_html or config.get('with_body_html', False):
                body_source_code = unescape(etree.tostring(node, encoding='utf-8').decode())
                node_info['body_html'] = body_source_code
            self.node_info[node_hash] = node_info
        self.calc_new_score()
        result = sorted(self.node_info.items(), key=lambda x: x[1]['score'], reverse=True)
        return result

    def count_text_tag(self, element, tag='p'):
        return len(element.xpath(f'.//{tag}'))

    def get_all_text_of_element(self, element_list):
        if not isinstance(element_list, list):
            element_list = [element_list]

        text_list = []
        for element in element_list:
            element_flag = element.getroottree().getpath(element)
            if element_flag in self.element_text_cache: # 直接读取缓存的数据，而不是再重复提取一次
                text_list = self.element_text_cache[element_flag]
            else:
                element_text_list = []
                for text in element.xpath('.//text()'):
                    text = text.strip()
                    if not text:
                        continue
                    clear_text = re.sub(' +', ' ', text, flags=re.S)
                    element_text_list.append(clear_text.replace('\n', ''))
                self.element_text_cache[element_flag] = element_text_list
                text_list.extend(element_text_list)
        return text_list

    def calc_text_density(self, element):
        """
        根据公式：

               Ti - LTi
        TDi = -----------
              TGi - LTGi


        Ti:节点 i 的字符串字数
        LTi：节点 i 的带链接的字符串字数
        TGi：节点 i 的标签数
        LTGi：节点 i 的带连接的标签数


        :return:
        """
        ti_text = '\n'.join(self.get_all_text_of_element(element))
        ti = len(ti_text)
        ti = self.increase_tag_weight(ti, element)
        lti = len(''.join(self.get_all_text_of_element(element.xpath('.//a'))))
        tgi = len(element.xpath('.//*'))
        ltgi = len(element.xpath('.//a'))
        if (tgi - ltgi) == 0:
            return {'density': 0, 'ti_text': ti_text, 'ti': ti, 'lti': lti, 'tgi': tgi, 'ltgi': ltgi}
        density = (ti - lti) / (tgi - ltgi)
        return {'density': density, 'ti_text': ti_text, 'ti': ti, 'lti': lti, 'tgi': tgi, 'ltgi': ltgi}

    def increase_tag_weight(self, ti, element):
        tag_class = element.get('class', '')
        if self.high_weight_keyword_pattern.search(tag_class):
            return 2 * ti
        return ti

    def calc_sbdi(self, text, ti, lti):
        """
                Ti - LTi
        SbDi = --------------
                 Sbi + 1

        SbDi: 符号密度
        Sbi：符号数量

        :return:
        """
        sbi = self.count_punctuation_num(text)
        sbdi = (ti - lti) / (sbi + 1)
        return sbdi or 1   # sbdi 不能为0，否则会导致求对数时报错。

    def count_punctuation_num(self, text):
        count = 0
        for char in text:
            if char in self.punctuation:
                count += 1
        return count

    def calc_new_score(self):
        """
        score = 1 * ndi * log10(text_tag_count + 2) * log(sbdi)

        1：在论文里面，这里使用的是 log(std)，但是每一个密度都乘以相同的对数，他们的相对大小是不会改变的，所以我们没有必要计算
        ndi：节点 i 的文本密度
        text_tag_count: 正文所在标签数。例如正文在<p></p>标签里面，这里就是 p 标签数，如果正文在<div></div>标签，这里就是 div 标签数
        sbdi：节点 i 的符号密度
        :param std:
        :return:
        """
        for node_hash, node_info in self.node_info.items():
            score = node_info['density'] * np.log10(node_info['text_tag_count'] + 2) * np.log(
                node_info['sbdi'])
            self.node_info[node_hash]['score'] = score
