# General News Extractor Changelog

## 0.2.4 (2020-10-06)

### Features

1. 预处理时，把 <footer>标签移除。

## 0.2.3 (2020-09-15)

### Bug fix

1. `USELESS_ATTR`对应的节点，只有 class 完全匹配才需要删除。之前包含就删除的匹配方式会导致 ifeng 的正文被删除。

## 0.2.2 (2020-08-02)

### Features

1. 指定列表页特征，自动提取列表页数据


## 0.2.1 (2020-06-27)

### Feature

1. 不再需要计算文本密度的标准差
2. 🚀减少重复计算，大幅度提升分析速度

## 0.2.0 (2020-06-06)

### Feature

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


## 0.1.9 (2020-03-11)

### Bug fix

1. 预处理可能会破坏 HTML 结构，导致用户自定义的 XPath 无法正确工作，因此需要把提取用户名、发布时间、标题的代码放在预处理之前。

## 0.1.8 (2020-02-21)

1. 感谢@止水提供的 meta 对应的新闻时间属性，现在会从 HTML 的 meta 数据中检查是否有发布时间。

## 0.1.7 (2020-02-13)

1. 在GeneralNewsExtractor().extract()方法中传入参数`author_xpath`和`publish_time_xpath`强行指定抓取作者与发布时间的位置。
2. 在.gne 配置文件中，通过如下两个配置分别指定作者与发布时间的 XPath

```yaml
author:
    xpath: //meta[@name="author"]/@content
publish_time:
    xpath: //em[@id="publish_time"]/text()
```

## 0.1.6 (2020-01-04)

1. 修复由于`node.getparent().remove()`会移除父标签中，位于自己后面的 text 的问题
2. 对于class 中含有`article`/`content`/`news_txt`/`post_text`的标签，增加权重
3. 使用更科学的方法移除无效标签

## 0.1.5 (2019-12-31)

通用参数可以通过 YAML、JSON 批量设置了。只需要在项目的根目录下创建一个 ``.gne`` ，就可以实现函数默认参数的功能。

## 0.1.4 (2019-12-29)

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

## 0.1.3 (2019-11-24)

1. 增加更多的 UselessAttr
2. 返回的结果包含`images`字段，里面的结果是一个列表，保存了正文中的所有图片 URL
3. 指定`with_body_html`参数，返回的数据中将会包含`body_html`字段，这是正文的 HTMl 源代码：

```python
...
result = GeneralNewsExtractor().extract(html, with_body_html=True)
body_html = result['body_html']
print(f'正文的网页源代码为：{body_html}')
```