import pprint
import glob
from gne import ListPageExtractor


html_list = glob.glob('test_list_page/163/1.html', recursive=True)
for html_file in html_list:
    with open(html_file, encoding='utf-8') as f:
        html = f.read()
    list_extractor = ListPageExtractor()
    result = list_extractor.extract(html,
                                    feature='//*[@id="index2016_wrap"]/div[1]/div[2]/div[2]/div[3]/div[2]/div[5]/div/ul/li[1]/div/div[1]/div/div[1]/h3/a')
    pprint.pprint(result)
