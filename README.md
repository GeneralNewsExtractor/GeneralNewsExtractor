# GNE (GeneralNewsExtractor)

[**中文文档**](README_CN.md)

![](https://github.com/GeneralNewsExtractor/GeneralNewsExtractor/raw/master/screenshots/logo.png)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=GeneralNewsExtractor/GeneralNewsExtractor&type=Date)](https://star-history.com/#GeneralNewsExtractor/GeneralNewsExtractor&Date)

## Introduction

GNE is a general-purpose news content extractor built in Python. It is based on the algorithm described in the paper ["Web Content Extraction Based on Text and Symbol Density"](https://kns.cnki.net/KCMS/detail/detail.aspx?dbcode=CJFQ&dbname=CJFDLAST2019&filename=GWDZ201908029&v=MDY4MTRxVHJXTTFGckNVUkxPZmJ1Wm5GQ2poVXJyQklqclBkTEc0SDlqTXA0OUhiWVI4ZVgxTHV4WVM3RGgxVDM=).

The algorithm is clean, logical, and effective. Since the paper only describes the algorithm without a concrete implementation, this project implements it in Python. It has been tested on major Chinese news sites (Toutiao, NetEase News, Sina News, iFeng, Tencent News, ReadHub, etc.) with nearly 100% accuracy.

## Current Status

Beyond the body text extraction described in the paper, GNE also supports automatic detection and extraction of **title**, **publish time**, and **author**.

This project is named "Extractor" rather than "Crawler" by design — the input is HTML, and the output is a dictionary. You are responsible for obtaining the HTML of target pages using your own methods.

**This project does not and will not provide any functionality to actively request HTML from websites.**

## Usage

### Online Demo

You can try GNE online at [http://gne.kingname.info/](http://gne.kingname.info/). Simply paste the rendered HTML into the text area and click the extract button. For more precise extraction, additional parameters can be provided. See the [API documentation](https://generalnewsextractor.readthedocs.io/zh_CN/latest/#api) for details.

### Installation

```bash
# Install via pip
pip install --upgrade gne

# Or install via pipenv
pipenv install gne
```

### Basic Usage

#### Extract Article Content

```python
from gne import GeneralNewsExtractor

html = '''Your rendered HTML code'''

extractor = GeneralNewsExtractor()
result = extractor.extract(html, noise_node_list=['//div[@class="comment-list"]'])
print(result)

# Output:
# {"title": "xxxx", "publish_time": "2019-09-10 11:12:13", "author": "yyy", "content": "zzzz", "images": ["/xxx.jpg", "/yyy.png"]}
```

For more details, see the [GNE documentation](https://generalnewsextractor.readthedocs.io/).

#### Extract List Pages (Beta)

```python
from gne import ListPageExtractor

html = '''Your rendered HTML code'''
list_extractor = ListPageExtractor()
result = list_extractor.extract(html, feature='XPath of any element in the list')
print(result)
```

### Advanced Usage

#### Custom Title XPath

If automatic title extraction fails, you can specify a custom XPath:

```python
from gne import GeneralNewsExtractor

extractor = GeneralNewsExtractor()
html = 'Your target page HTML'
result = extractor.extract(html, title_xpath='//h5/text()')
print(result)
```

#### Noise Removal

Some news pages contain comments that may look more like body text than the actual article. Use the `noise_node_list` parameter to remove interfering elements before extraction:

```python
result = extractor.extract(html, noise_node_list=['//div[@class="comment-list"]'])
```

`noise_node_list` accepts a list of XPath expressions, each targeting an element to be removed during preprocessing.

### Development Setup

```bash
git clone https://github.com/kingname/GeneralNewsExtractor.git
cd GeneralNewsExtractor
pipenv install
pipenv shell
python3 example.py
```

### Notes

- The `example.py` file provides basic usage examples.
- Test code is located in the `tests` directory.
- The input HTML must be **JavaScript-rendered HTML**, not raw page source. This means GNE works with both server-side rendered and Ajax-loaded content.
- To manually test a new page, open it in Chrome, go to Developer Tools, locate the `<html>` tag in the Elements tab, right-click and select `Copy` > `Copy OuterHTML`.

![](https://github.com/kingname/GeneralNewsExtractor/blob/master/screenshots/2019-09-08-22-20-33.png)

![](https://github.com/kingname/GeneralNewsExtractor/blob/master/screenshots/2019-09-08-22-21-49.png)

- You can also use Puppeteer/Pyppeteer, Selenium, or any other method to obtain the JavaScript-rendered source code.
- **List page extraction is an experimental feature and should not be used in production.** You can use Chrome DevTools' `Copy XPath` to copy the XPath of any item in the list. GNE will automatically find other items in the same list.

![](https://github.com/kingname/GeneralNewsExtractor/blob/master/screenshots/2020-08-02-17-07-19.png)

## Screenshots

### NetEase News

![](https://github.com/kingname/GeneralNewsExtractor/blob/master/screenshots/WX20191125-231230.png)

### Toutiao

![](https://github.com/kingname/GeneralNewsExtractor/blob/master/screenshots/WX20191125-225851.png)

### Sina News

![](https://github.com/kingname/GeneralNewsExtractor/blob/master/screenshots/WX20191125-231506.png)

### iFeng

![](https://github.com/kingname/GeneralNewsExtractor/blob/master/screenshots/WX20191126-004218.png)

### NetEase News List Page

![](https://github.com/kingname/GeneralNewsExtractor/blob/master/screenshots/WX20200802-170137@2x.png)

## Documentation

[GNE FAQ & Q&A](https://github.com/kingname/GeneralNewsExtractor/wiki/GeneralNewsExtractor-Q&A)

## Known Issues

1. GNE is designed for news article pages. It may not work well on non-news pages or photo gallery articles.
2. The author field may be empty if the article does not specify an author or if the author pattern is not covered by the existing regular expressions.

## Todo

* ~~Use a configuration file for constants instead of hard-coding them.~~
* ~~Allow custom patterns for time and author extraction.~~
* ~~News article list page extraction.~~
* Support multi-page articles by accepting a list of HTMLs and concatenating the extracted content.
* ~~Optimize extraction speed.~~
* ~~Test on more news websites.~~
* ...

## Community

- WeChat: Add the author `mekingname` and mention "GNE" to join the group.
- Telegram: [https://t.me/joinchat/Bc5swww_XnVR7pEtDUl1vw](https://t.me/joinchat/Bc5swww_XnVR7pEtDUl1vw)

## Acknowledgements

@bigbrother666sh
