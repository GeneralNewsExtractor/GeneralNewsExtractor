from .utils import pre_parse, remove_noise_node
from gne.extractor import ContentExtractor, TitleExtractor, TimeExtractor, AuthorExtractor


class GeneralNewsExtractor:
    def __init__(self):
        self.content_extractor = ContentExtractor()
        self.title_extractor = TitleExtractor()
        self.author_extractor = AuthorExtractor()
        self.time_extractor = TimeExtractor()

    def extract(self, html, noise_node_list=None):
        element = pre_parse(html)
        remove_noise_node(element, noise_node_list)
        content = self.content_extractor.extract(element)
        title = self.title_extractor.extract(element)
        publish_time = self.time_extractor.extractor(element)
        author = self.author_extractor.extractor(element)
        return {'title': title,
                'author': author,
                'publish_time': publish_time,
                'content': content[0][1]['text']}
