from gne.utils import pre_parse, remove_noise_node, config, html2element, normalize_text
from gne.extractor import ContentExtractor, TitleExtractor, TimeExtractor, AuthorExtractor, ListExtractor
from selenium import webdriver
import asyncio
import random
import time
import warnings

warnings.filterwarnings("ignore")
import aiohttp
import asyncio


class GeneralNewsExtractor:

    async def fetch(self, urls):
        async with aiohttp.request('GET', urls) as resp:
            assert resp.status == 200
            return await resp.text()

    async def url_to_sourcecode(self, queue, urls):

        s = time.perf_counter()
        for i in urls:
            html = await GeneralNewsExtractor().fetch(i)
            await queue.put(html)
            await asyncio.sleep(random.random())
        # await client.close()
        await queue.put(None)
        elapsed = time.perf_counter() - s
        print(f"{__file__} executed in {elapsed:0.2f} seconds.")

    async def extract(self,
                      queue=None,
                      # html,
                      title_xpath='',
                      author_xpath='',
                      publish_time_xpath='',
                      host='',
                      body_xpath='',
                      noise_node_list=None,
                      with_body_html=False):

        # print("Naaru!")
        # 对 HTML 进行预处理可能会破坏 HTML 原有的结构，导致根据原始 HTML 编写的 XPath 不可用
        # 因此，如果指定了 title_xpath/author_xpath/publish_time_xpath，那么需要先提取再进行
        # 预处理
        # while True:
        # # wait for an item from the producer
        #     item = await queue.get()
        #     if item is None:
        #     # the producer emits None to indicate that it is done
        #         break

        while True:
            item = await queue.get()
            if item is None:
                # the producer emits None to indicate that it is done
                break
            html = item
            normal_html = normalize_text(html)
            element = html2element(normal_html)
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

            print(result)


class ListPageExtractor:
    def extract(self, feature):
        html = GeneralNewsExtractor().url_to_sourcecode()
        normalize_html = normalize_text(html)
        element = html2element(normalize_html)
        extractor = ListExtractor()
        return extractor.extract(element, feature)


urls = eval(input("Enter the list of url ['example.com', 'example.in']:"))

# loop = asyncio.get_event_loop()
# loop.run_until_complete(o.extract())

loop = asyncio.get_event_loop()
queue = asyncio.Queue(loop=loop)
producer_coro = GeneralNewsExtractor().url_to_sourcecode(queue, urls)
consumer_coro = GeneralNewsExtractor().extract(queue)
loop.run_until_complete(asyncio.gather(producer_coro, consumer_coro))
loop.close()