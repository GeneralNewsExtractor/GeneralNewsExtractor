import re
import numpy as np
from lxml.html import HtmlElement


class ContentExtractor:
    def __init__(self, content_tag='p'):
        """

        :param content_tag: 正文内容在哪个标签里面
        """
        self.content_tag = content_tag
        self.node_info = {}
        self.punctuation = set('''！，。？；：“”‘’《》%（）,.?:;'"!%()''')  # 常见的中英文标点符号

    def extract(self, selector):
        body = selector.xpath('//body')[0]
        for node in self.iter_node(body):
            node_hash = hash(node)
            density_info = self.calc_text_density(node)
            text_density = density_info['density']
            ti_text = density_info['ti_text']
            text_tag_count = self.count_text_tag(node, tag='p')
            sbdi = self.calc_sbdi(ti_text, density_info['ti'], density_info['lti'])
            self.node_info[node_hash] = {'node': node,
                                         'density': text_density,
                                         'text': ti_text,
                                         'text_tag_count': text_tag_count,
                                         'sbdi': sbdi}
        std = self.calc_standard_deviation()
        self.calc_new_score(std)
        result = sorted(self.node_info.items(), key=lambda x: x[1]['score'], reverse=True)
        return result

    def count_text_tag(self, element, tag='p'):
        return len(element.xpath(f'.//{tag}'))

    def get_all_text_of_element(self, element_list):
        text_list = []
        if not isinstance(element_list, list):
            element_list = [element_list]

        for element in element_list:
            for text in element.xpath('.//text()'):
                text = text.strip()
                if not text:
                    continue
                clear_text = re.sub(' +', '', text, flags=re.S)
                text_list.append(clear_text.replace('\n', ''))
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
        lti = len(''.join(self.get_all_text_of_element(element.xpath('.//a'))))
        tgi = len(element.xpath('.//*'))
        ltgi = len(element.xpath('.//a'))
        if (tgi - ltgi) == 0:
            return {'density': 0, 'ti_text': ti_text, 'ti': ti, 'lti': lti}
        density = (ti - lti) / (tgi - ltgi)
        return {'density': density, 'ti_text': ti_text, 'ti': ti, 'lti': lti}

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
        return sbdi or 1  # sbdi 不能为0，否则会导致求对数时报错。

    def count_punctuation_num(self, text):
        count = 0
        for char in text:
            if char in self.punctuation:
                count += 1
        return count

    def iter_node(self, element: HtmlElement):
        yield element
        for sub_element in element:
            if isinstance(sub_element, HtmlElement):
                yield from self.iter_node(sub_element)

    def calc_standard_deviation(self):
        score_list = [x['density'] for x in self.node_info.values()]
        std = np.std(score_list, ddof=1)
        return std

    def calc_new_score(self, std):
        for node_hash, node_info in self.node_info.items():
            score = np.log(std) * node_info['density'] * np.log10(node_info['text_tag_count'] + 2) * np.log(
                node_info['sbdi'])
            self.node_info[node_hash]['score'] = score
