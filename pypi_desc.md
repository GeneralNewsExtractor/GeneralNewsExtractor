# GNE: 通用新闻网站正文抽取器

GeneralNewsExtractor（GNE）是一个通用新闻网站正文抽取模块，输入一篇新闻网页的 HTML， 输出正文内容、标题、作者、发布时间、正文中的图片地址和正文所在的标签源代码。GNE在提取今日头条、网易新闻、游民星空、 观察者网、凤凰网、腾讯新闻、ReadHub、新浪新闻等数百个中文新闻网站上效果非常出色，几乎能够达到100%的准确率。

使用方式也非常简单：

```python
from gne import GeneralNewsExtractor

extractor = GeneralNewsExtractor()
html = '网站源代码'
result = extractor.extract(html)
print(result)
```

## 安装

```
pip install gne
```

## 文档

https://generalnewsextractor.readthedocs.io/

## 帮助 GNE 变得更好

https://github.com/kingname/GeneralNewsExtractor