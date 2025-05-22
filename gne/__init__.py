from .exceptions import NoContentException
from .utils import pre_parse, remove_noise_node, config, html2element, normalize_text, fix_html
from gne.extractor import ContentExtractor, TitleExtractor, TimeExtractor, AuthorExtractor, ListExtractor, MetaExtractor

__version__ = "0.3.1"
__author__ = "Kingname"


class GeneralNewsExtractor:
    def extract(self,
                html,
                title_xpath='',
                author_xpath='',
                publish_time_xpath='',
                host='',
                body_xpath='',
                normalize=False,
                noise_node_list=None,
                with_body_html=False,
                use_visiable_info=False):

        # 对 HTML 进行预处理可能会破坏 HTML 原有的结构，导致根据原始 HTML 编写的 XPath 不可用
        # 因此，如果指定了 noise_node/title_xpath/author_xpath/publish_time_xpath，那么需要先提取再进行
        # 预处理
        html = fix_html(html)
        remove_noise_node(element, noise_node_list)
        if normalize:
            normal_html = normalize_text(html)
        else:
            normal_html = html
        element = html2element(normal_html)
        meta_content = MetaExtractor().extract(element)
        title = TitleExtractor().extract(element, title_xpath=title_xpath)
        publish_time = TimeExtractor().extractor(element, publish_time_xpath=publish_time_xpath)
        author = AuthorExtractor().extractor(element, author_xpath=author_xpath)
        element = pre_parse(element)
        
        content = ContentExtractor().extract(element,
                                             host=host,
                                             with_body_html=with_body_html,
                                             body_xpath=body_xpath,
                                             use_visiable_info=use_visiable_info)
        if not content:
            raise NoContentException('无法提取正文！')
        result = {'title': title,
                  'author': author,
                  'publish_time': publish_time,
                  'content': content[0][1]['text'],
                  'images': content[0][1]['images'],
                  'meta': meta_content
                  }
        if with_body_html or config.get('with_body_html', False):
            result['body_html'] = content[0][1]['body_html']
        return result


class ListPageExtractor:
    def extract(self, html, feature):
        normalize_html = normalize_text(html)
        element = html2element(normalize_html)
        extractor = ListExtractor()
        return extractor.extract(element, feature)

