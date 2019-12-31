from .utils import pre_parse, remove_noise_node, config
from gne.extractor import ContentExtractor, TitleExtractor, TimeExtractor, AuthorExtractor


class GeneralNewsExtractor:
    def extract(self, html, title_xpath='', host='', noise_node_list=None, with_body_html=False):
        element = pre_parse(html)
        remove_noise_node(element, noise_node_list)
        content = ContentExtractor().extract(element, host, with_body_html)
        title = TitleExtractor().extract(element, title_xpath=title_xpath)
        publish_time = TimeExtractor().extractor(element)
        author = AuthorExtractor().extractor(element)
        result = {'title': title,
                  'author': author,
                  'publish_time': publish_time,
                  'content': content[0][1]['text'],
                  'images': content[0][1]['images']}
        if with_body_html or config.get('with_body_html', False):
            result['body_html'] = content[0][1]['body_html']
        return result
