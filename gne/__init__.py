from .utils import pre_parse, remove_noise_node
from gne.extractor import ContentExtractor, TitleExtractor, TimeExtractor, AuthorExtractor


class GeneralNewsExtractor:
    def extract(self, html, title_xpath='', noise_node_list=None):
        element = pre_parse(html)
        remove_noise_node(element, noise_node_list)
        content = ContentExtractor().extract(element)
        title = TitleExtractor().extract(element, title_xpath=title_xpath)
        publish_time = TimeExtractor().extractor(element)
        author = AuthorExtractor().extractor(element)
        return {'title': title,
                'author': author,
                'publish_time': publish_time,
                'content': content[0][1]['text']}
