import json
import glob
from utils import pre_parse, remove_noise_node
from extractor import ContentExtractor, TitleExtractor, TimeExtractor, AuthorExtractor


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


if __name__ == '__main__':
    html_list = glob.glob('**/*.html', recursive=True)
    for html_file in html_list:
        with open(html_file, encoding='utf-8') as f:
            html = f.read()
        extractor = GeneralNewsExtractor()
        result = extractor.extract(html, noise_node_list=['//div[@class="comment-list"]'])
        print(f'>>>>>>>>>>>>>{html_file}>>>>>>>>>>>>>')
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
