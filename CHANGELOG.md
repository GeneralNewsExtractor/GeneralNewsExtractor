# General News Extractor Changelog

## 0.4.1 (2026-03-02)

### Bug fix

1. 修复 USELESS_ATTR 子串匹配导致正文被误删的严重 bug：短关键词（如 `ad`、`nav`）会误匹配含有这些子串的正常 class/id（如 `padding`、`canvas`、`headline`），改为按 `-` `_` 空格拆分后的词级匹配
2. 添加 meta author 校验（`_is_valid_author`），过滤纯数字、邮箱、占位符等无效作者值
3. 添加日期校验（`_is_valid_date`），拒绝月份 >12 或日期 >31 的匹配结果，避免版本号等被误识别为日期

## 0.4.0 (2026-03-02)

### Performance

1. 移除 numpy 依赖，改用标准库 `math` 模块计算对数，减少安装体积、加快 import 速度
2. 预编译所有正则表达式（`DATETIME_PATTERN`、`AUTHOR_PATTERN`、BR 标签、高权重关键词），避免运行时重复编译
3. `GeneralNewsExtractor` 预创建各 extractor 实例，`extract()` 调用间复用，不再每次 new
4. 最长公共子串算法改为滚动数组，空间复杂度从 O(n*m) 降至 O(min(n,m))
5. `count_punctuation_num` 改为生成器表达式，更 Pythonic

### Bug fix

1. 修复正则表达式字符类 bug：`[-|/|.]` → `[-/.]`、`[：|:| |丨|/]` → `[：: 丨/]`，`|` 在 `[]` 中是字面量而非"或"
2. 修复 `normalize_node` 中匹配到 USELESS_ATTR 后 `break` 退出整个循环的 bug，改为收集后批量删除
3. 修复 `normalize_node` 遍历过程中修改树结构的问题，先将 `iter_node` 结果转为 list
4. 修复 `ArticleClassifier` 中 `classfy_by_weight` 拼写错误及缺失的 return 语句
5. 清理 `MetaExtractor` 中未实现的 `extract_meta` 方法

### Enhancements

1. 新增 `og:title` meta 标签提取作为标题候选
2. 新增 `<meta name="author">` 提取，优先于正则匹配
3. 新增 `date`、`DC.date` 等 meta 时间 XPath
4. USELESS_TAG 移除 `blockquote`（新闻正文常用引用），新增 `nav`、`aside`
5. USELESS_ATTR 新增 `sidebar`、`navigation`、`nav`、`breadcrumb`、`ad`、`advertisement`，并改为子串匹配同时检查 `id` 属性
6. HIGH_WEIGHT_ARRT_KEYWORD 新增 `post_body`、`entry-content`、`article-body`、`story-body`、`main-content`

### Infrastructure

1. 依赖管理从 pipenv 迁移到 uv，使用 `pyproject.toml` + `uv.lock`
2. 删除 `Pipfile`、`Pipfile.lock`、`setup.py`、`setup.cfg`、`requirements.txt`、`MANIFEST.in`
3. 升级 lxml 最低版本至 4.9.1（修复 CVE-2022-2309）
4. Python 版本支持范围更新为 3.8 - 3.13

## 0.3.1 (2024-04-17)

### Bug fix

有一些网站源代码不规范，在html中间突然出现</html>。末尾又出现一次</html>.这种情况下，会导致解析出错。现在已经修复。

## 0.3.0 (2021-10-07)

### New Feature

1. 基于可视化区域，更准确地识别正文

### Bug fix

* 修复下面这种情况时，无法正确寻找正文的 bug

```html
<div>
我是正文我是正文我是正文<a href="xxx">关键词1</a>我是正文我是正文我是正文我是正文
我是正文我是正文我是正文我是正文我是正文<a href="xxx">关键词2</a>我是正文我是正文
我是正文
</div>
```

* 统计一个标签下面的 p 标签的时候，应该把这个标签下面的直接文档数也统计进去

## 0.2.6 (2021-02-17)

### Bug fix

1. 修复 extract_by_htag_and_title 在发现 H 标签中的文本与 title 标签的文本在最小公共子串长度小于4时被认为是标题的问题。

## 0.2.5 (2020-12-21)

### Bug fix

1. 在使用 title 标签提取标题时，对于分隔符-_|分割的第一段内容，必须要大于4个字符才当做标题，否则会返回整个 title 标签的文本。

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