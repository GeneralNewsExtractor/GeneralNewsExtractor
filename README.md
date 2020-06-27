## 项目起源

开发这个项目，源自于我在知网发现了一篇关于自动化抽取新闻类网站正文的算法论文——[《基于文本及符号密度的网页正文提取方法》](https://kns.cnki.net/KCMS/detail/detail.aspx?dbcode=CJFQ&dbname=CJFDLAST2019&filename=GWDZ201908029&v=MDY4MTRxVHJXTTFGckNVUkxPZmJ1Wm5GQ2poVXJyQklqclBkTEc0SDlqTXA0OUhiWVI4ZVgxTHV4WVM3RGgxVDM=)）

这篇论文中描述的算法看起来简洁清晰，并且符合逻辑。但由于论文中只讲了算法原理，并没有具体的语言实现，所以我使用 Python 根据论文实现了这个抽取器。并分别使用今日头条、网易新闻、游民星空、观察者网、凤凰网、腾讯新闻、ReadHub、新浪新闻做了测试，发现提取效果非常出色，几乎能够达到100%的准确率。

## 项目现状

在论文中描述的正文提取基础上，我增加了标题、发布时间和文章作者的自动化探测与提取功能。

目前这个项目是一个非常非常早期的 Demo，发布出来是希望能够尽快得到大家的使用反馈，从而能够更好地有针对性地进行开发。

本项目取名为`抽取器`，而不是`爬虫`，是为了规避不必要的风险，因此，本项目的输入是 HTML，输出是一个字典。请自行使用恰当的方法获取目标网站的 HTML。

**本项目现在不会，将来也不会提供主动请求网站 HTML 的功能。**

## 如何使用

### 在线体验

如果你想先体验 GNE 的提取效果，那么你可以访问[http://122.51.39.219/](http://122.51.39.219/)。
一般情况下，你只需要把网页粘贴到最上面的多行文本框中，然后点`提取`按钮即可。通过附加更多的参数，可以让提取更精确。具体
参数的写法与作用，请参阅 [API](https://generalnewsextractor.readthedocs.io/zh_CN/latest/#api)

### 使用环境

如果你想体验 GNE 的功能，请按照如下步骤进行：

1. 安装 GNE

```bash

# 以下两种方案任选一种即可

# 使用 pip 安装
pip install --upgrade gne

# 使用 pipenv 安装
pipenv install gne

```

2. 使用 GNE

```python
>>> from gne import GeneralNewsExtractor

>>> html = '''经过渲染的网页 HTML 代码'''

>>> extractor = GeneralNewsExtractor()
>>> result = extractor.extract(html, noise_node_list=['//div[@class="comment-list"]'])
>>> print(result)

{"title": "xxxx", "publish_time": "2019-09-10 11:12:13", "author": "yyy", "content": "zzzz", "images": ["/xxx.jpg", "/yyy.png"]}
```

更多使用说明，请参阅 [GNE 的文档](https://generalnewsextractor.readthedocs.io/)


### 开发环境

如果你需要参与本项目的开发，请按照如下步骤进行。

本项目使用 `Pipenv`管理 Python 的第三方库。如果你不知道 `Pipenv` 是什么，请[点我跳转](https://github.com/pypa/pipenv)。

安装完成`Pipenv`以后，按照如下步骤运行代码：

```bash
git clone https://github.com/kingname/GeneralNewsExtractor.git
cd GeneralNewsExtractor
pipenv install
pipenv shell
python3 example.py
```

### 特别说明

项目代码中的`example.py`提供了本项目的基本使用示例。

* 本项目的测试代码在`tests`文件夹中
* 本项目的输入 HTML 为经过 JavaScript 渲染以后的 HTML，而不是普通的网页源代码。所以无论是后端渲染、Ajax 异步加载都适用于本项目。
* 如果你要手动测试新的目标网站或者目标新闻，那么你可以在 Chrome 浏览器中打开对应页面，然后开启`开发者工具`，如下图所示：

![](https://github.com/kingname/GeneralNewsExtractor/blob/master/screenshots/2019-09-08-22-20-33.png)

在`Elements`标签页定位到`<html>`标签，并右键，选择`Copy`-`Copy OuterHTML`，如下图所示

![](https://github.com/kingname/GeneralNewsExtractor/blob/master/screenshots/2019-09-08-22-21-49.png)

* 当然，你可以使用 Puppeteer/Pyppeteer、Selenium 或者其他任何方式获取目标页面的`JavaScript渲染后的`源代码。

* 获取到源代码以后，通过如下代码提取信息：

``` python
from gne import GeneralNewsExtractor

extractor = GeneralNewsExtractor()
html = '你的目标网页正文'
result = extractor.extract(html)
print(result)
```

* 如果标题自动提取失败了，你可以指定 XPath：

```python
from gne import GeneralNewsExtractor

extractor = GeneralNewsExtractor()
html = '你的目标网页正文'
result = extractor.extract(html, title_xpath='//h5/text()')
print(result)
```

对大多数新闻页面而言，以上的写法就能够解决问题了。

但某些新闻网页下面会有评论，评论里面可能存在长篇大论，它们会看起来比真正的新闻正文更像是正文，因此`extractor.extract()`方法还有一个默认参数`noise_node_list`，用于在网页预处理时提前把评论区域整个移除。

`noise_mode_list`的值是一个列表，列表里面的每一个元素都是 XPath，对应了你需要提前移除的，可能会导致干扰的目标标签。

例如，`观察者网`下面的评论区域对应的Xpath 为`//div[@class="comment-list"]`。所以在提取观察者网时，为了防止评论干扰，就可以加上这个参数：

```python
result = extractor.extract(html, noise_node_list=['//div[@class="comment-list"]'])
```

`test`文件夹中的网页的提取结果，请查看`result.txt`。

## 运行截图

### 网易新闻

![](https://github.com/kingname/GeneralNewsExtractor/blob/master/screenshots/WX20191125-231230.png)

### 今日头条

![](https://github.com/kingname/GeneralNewsExtractor/blob/master/screenshots/WX20191125-225851.png)

### 新浪新闻

![](https://github.com/kingname/GeneralNewsExtractor/blob/master/screenshots/WX20191125-231506.png)

### 凤凰网

![](https://github.com/kingname/GeneralNewsExtractor/blob/master/screenshots/WX20191126-004218.png)

## 项目文档

[GNE 常见问题 Q&A](https://github.com/kingname/GeneralNewsExtractor/wiki/GeneralNewsExtractor-Q&A)

## 已知问题

1. 目前本项目只适用于新闻页的信息提取。如果目标网站不是新闻页，或者是今日头条中的相册型文章，那么抽取结果可能不符合预期。
2. 可能会有一些新闻页面出现抽取结果中的作者为空字符串的情况，这可能是由于文章本身没有作者，或者使用了已有正则表达式没有覆盖到的情况。

## Changelog

### 2020.06.27

1. 不再需要计算文本密度的标准差
2. 🚀减少重复计算，大幅度提升分析速度

### 2020.06.06

1. 优化标题提取逻辑，根据@止水 和 @asyncins 的建议，通过对比 //title/text()中的文本与 <h> 标签中的文本，提取出标题。
2. 增加 `body_xpath`参数，精确定义正文所在的位置，强力避免干扰。

例如对于澎湃新闻，在不设置`body_xpath`参数时：

```python
result = extractor.extract(html,
                           host='https://www.xxx.com',
                           noise_node_list=['//div[@class="comment-list"]',
                                            '//*[@style="display:none"]',
                                            '//div[@class="statement"]'
                                            ])
```

提取效果如下：

![](https://kingname-1257411235.cos.ap-chengdu.myqcloud.com/2020-06-06-11-51-44.png)

设置了`body_xpath`以后：

```python
result = extractor.extract(html,
                           host='https://www.xxx.com',
                           body_xpath='//div[@class="news_txt"]',  # 缩小正文提取范围
                           noise_node_list=['//div[@class="comment-list"]',
                                            '//*[@style="display:none"]',
                                            '//div[@class="statement"]'
                                            ])
```

结果如下：

![](https://kingname-1257411235.cos.ap-chengdu.myqcloud.com/2020-06-06-11-53-30.png)


### 2020.03.11

1. 预处理可能会破坏 HTML 结构，导致用户自定义的 XPath 无法正确工作，因此需要把提取用户名、发布时间、标题的代码放在预处理之前。

### 2020.02.21

1. 感谢@止水提供的 meta 对应的新闻时间属性，现在会从 HTML 的 meta 数据中检查是否有发布时间。

### 2020.02.13

1. 在GeneralNewsExtractor().extract()方法中传入参数`author_xpath`和`publish_time_xpath`强行指定抓取作者与发布时间的位置。
2. 在.gne 配置文件中，通过如下两个配置分别指定作者与发布时间的 XPath

```yaml
author:
    xpath: //meta[@name="author"]/@content
publish_time:
    xpath: //em[@id="publish_time"]/text()
```

### 2020.01.04

1. 修复由于`node.getparent().remove()`会移除父标签中，位于自己后面的 text 的问题
2. 对于class 中含有`article`/`content`/`news_txt`/`post_text`的标签，增加权重
3. 使用更科学的方法移除无效标签

### 2019.12.31

通用参数可以通过 YAML、JSON 批量设置了。只需要在项目的根目录下创建一个 ``.gne`` ，就可以实现函数默认参数的功能。

### 2019.12.29

1. 现在可以通过传入参数`host`来把提取的图片url 拼接为绝对路径

例如：

```python
extractor = GeneralNewsExtractor()
result = extractor.extract(html,
                           host='https://www.xxx.com')
```

返回数据中：

```python
{
    ...
    "images": [
        "https://www.xxx.com/W020190918234243033577.jpg"
      ]
}
```

### 2019.11.24

1. 增加更多的 UselessAttr
2. 返回的结果包含`images`字段，里面的结果是一个列表，保存了正文中的所有图片 URL
3. 指定`with_body_html`参数，返回的数据中将会包含`body_html`字段，这是正文的 HTMl 源代码：

```python
...
result = GeneralNewsExtractor().extract(html, with_body_html=True)
body_html = result['body_html']
print(f'正文的网页源代码为：{body_html}')
```

## Todo

* ~~使用一个配置文件来存放常量数据，而不是直接 Hard Code 写在代码中。~~
* ~~允许自定义时间、作者的提取Pattern~~
* 新闻文章列表页提取
* 对于多页的新闻，允许传入一个 HTML 列表，GNE 解析以后，自动拼接为完整的新闻正文
* 优化内容提取速度
* 测试更多新闻网站
* ……

## 交流沟通

如果您觉得GNE对您的日常开发或公司有帮助，请加作者微信 mxqiuchen（或扫描下方二维码） 并注明"GNE"，作者会将你拉入群。

![](https://kingname-1257411235.cos.ap-chengdu.myqcloud.com/IMG_3729_2.JPG)

验证消息：`GNE`

如果你不用微信，那么可以加入 Telegram 群：[https://t.me/joinchat/Bc5swww_XnVR7pEtDUl1vw](https://t.me/joinchat/Bc5swww_XnVR7pEtDUl1vw)


## 论文修订

在使用 Python 实现这个抽取器的过程中，我发现论文里面的公式和方法存在一些纰漏，会导致部分节点报错。我将会单独写几篇文章来介绍这里的修改。请关注我的微信公众号：未闻Code：

![](https://kingname-1257411235.cos.ap-chengdu.myqcloud.com/wechatplatform.jpg)


