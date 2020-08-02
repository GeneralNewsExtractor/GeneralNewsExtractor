from .utils import pre_parse, remove_noise_node, config, html2element
from gne.extractor import ContentExtractor, TitleExtractor, TimeExtractor, AuthorExtractor, ListExtractor


class GeneralNewsExtractor:
    def extract(self,
                html,
                title_xpath='',
                author_xpath='',
                publish_time_xpath='',
                host='',
                body_xpath='',
                noise_node_list=None,
                with_body_html=False):

        # 对 HTML 进行预处理可能会破坏 HTML 原有的结构，导致根据原始 HTML 编写的 XPath 不可用
        # 因此，如果指定了 title_xpath/author_xpath/publish_time_xpath，那么需要先提取再进行
        # 预处理
        element = html2element(html)
        title = TitleExtractor().extract(element, title_xpath=title_xpath)
        publish_time = TimeExtractor().extractor(element, publish_time_xpath=publish_time_xpath)
        author = AuthorExtractor().extractor(element, author_xpath=author_xpath)
        element = pre_parse(element)
        remove_noise_node(element, noise_node_list)
        content = ContentExtractor().extract(element,
                                             host=host,
                                             with_body_html=with_body_html,
                                             body_xpath=body_xpath)
        result = {'title': title,
                  'author': author,
                  'publish_time': publish_time,
                  'content': content[0][1]['text'],
                  'images': content[0][1]['images']
                  }
        if with_body_html or config.get('with_body_html', False):
            result['body_html'] = content[0][1]['body_html']
        return result


class ListPageExtractor:
    def extract(self, html, feature):
        element = html2element(html)
        extractor = ListExtractor()
        return extractor.extract(element, feature)
