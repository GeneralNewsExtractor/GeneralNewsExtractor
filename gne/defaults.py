import re

AUTHOR_PATTERN_STR = [
            r"责编[：: 丨/]\s*([\u4E00-\u9FA5a-zA-Z0-9][\u4E00-\u9FA5a-zA-Z]{1,19})[^\u4E00-\u9FA5:：]",
            r"责任编辑[：: 丨/]\s*([\u4E00-\u9FA5a-zA-Z0-9][\u4E00-\u9FA5a-zA-Z]{1,19})[^\u4E00-\u9FA5:：]",
            r"作者[：: 丨/]\s*([\u4E00-\u9FA5a-zA-Z0-9][\u4E00-\u9FA5a-zA-Z]{1,19})[^\u4E00-\u9FA5:：]",
            r"编辑[：: 丨/]\s*([\u4E00-\u9FA5a-zA-Z0-9][\u4E00-\u9FA5a-zA-Z]{1,19})[^\u4E00-\u9FA5:：]",
            r"文[：: 丨/]\s*([\u4E00-\u9FA5a-zA-Z0-9][\u4E00-\u9FA5a-zA-Z]{1,19})[^\u4E00-\u9FA5:：]",
            r"原创[：: 丨/]\s*([\u4E00-\u9FA5a-zA-Z0-9][\u4E00-\u9FA5a-zA-Z]{1,19})[^\u4E00-\u9FA5:：]",
            r"撰文[：: 丨/]\s*([\u4E00-\u9FA5a-zA-Z0-9][\u4E00-\u9FA5a-zA-Z]{1,19})[^\u4E00-\u9FA5:：]",
            r"来源[：: 丨/]\s*([\u4E00-\u9FA5a-zA-Z0-9][\u4E00-\u9FA5a-zA-Z]{1,19})[^\u4E00-\u9FA5:：<]",
]

AUTHOR_PATTERN = [re.compile(p) for p in AUTHOR_PATTERN_STR]

DATETIME_PATTERN_STR = [
    r"(\d{4}[-/.]\d{1,2}[-/.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
    r"(\d{4}[-/.]\d{1,2}[-/.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
    r"(\d{4}[-/.]\d{1,2}[-/.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9])",
    r"(\d{4}[-/.]\d{1,2}[-/.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9])",
    r"(\d{4}[-/.]\d{1,2}[-/.]\d{1,2}\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
    r"(\d{2}[-/.]\d{1,2}[-/.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
    r"(\d{2}[-/.]\d{1,2}[-/.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
    r"(\d{2}[-/.]\d{1,2}[-/.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9])",
    r"(\d{2}[-/.]\d{1,2}[-/.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9])",
    r"(\d{2}[-/.]\d{1,2}[-/.]\d{1,2}\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
    r"(\d{4}年\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
    r"(\d{4}年\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
    r"(\d{4}年\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9])",
    r"(\d{4}年\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9])",
    r"(\d{4}年\d{1,2}月\d{1,2}日\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
    r"(\d{2}年\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
    r"(\d{2}年\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
    r"(\d{2}年\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9])",
    r"(\d{2}年\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9])",
    r"(\d{2}年\d{1,2}月\d{1,2}日\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
    r"(\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
    r"(\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
    r"(\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9])",
    r"(\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9])",
    r"(\d{1,2}月\d{1,2}日\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
    r"(\d{4}[-/.]\d{1,2}[-/.]\d{1,2})",
    r"(\d{2}[-/.]\d{1,2}[-/.]\d{1,2})",
    r"(\d{4}年\d{1,2}月\d{1,2}日)",
    r"(\d{2}年\d{1,2}月\d{1,2}日)",
    r"(\d{1,2}月\d{1,2}日)"
]

DATETIME_PATTERN = [re.compile(p) for p in DATETIME_PATTERN_STR]

TITLE_HTAG_XPATH = '//h1//text() | //h2//text() | //h3//text() | //h4//text()'

TITLE_SPLIT_CHAR_PATTERN = '[-_|]'

USELESS_TAG = ['style', 'script', 'link', 'video', 'iframe', 'source', 'picture', 'header',
               'footer', 'nav', 'aside']

# if one tag in the follow list does not contain any child node nor content, it could be removed
TAGS_CAN_BE_REMOVE_IF_EMPTY = ['section', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span']

USELESS_ATTR = {
                'share',
                'contribution',
                'copyright',
                'copy-right',
                'disclaimer',
                'recommend',
                'related',
                'footer',
                'comment',
                'social',
                'submeta',
                'report-infor',
                'header_toolbar',
                'sidebar',
                'navigation',
                'nav',
                'breadcrumb',
                'ad',
                'advertisement',
                }


HIGH_WEIGHT_ARRT_KEYWORD = ['content',
                            'article',
                            'news_txt',
                            'pages_content',
                            'post_text',
                            'post_body',
                            'entry-content',
                            'article-body',
                            'story-body',
                            'main-content']


PUBLISH_TIME_META = [  # 部分特别规范的新闻网站，可以直接从 HTML 的 meta 数据中获得发布时间
    '//meta[starts-with(@property, "rnews:datePublished")]/@content',
    '//meta[starts-with(@property, "article:published_time")]/@content',
    '//meta[starts-with(@property, "og:published_time")]/@content',
    '//meta[starts-with(@property, "og:release_date")]/@content',
    '//meta[starts-with(@itemprop, "datePublished")]/@content',
    '//meta[starts-with(@itemprop, "dateUpdate")]/@content',
    '//meta[starts-with(@name, "OriginalPublicationDate")]/@content',
    '//meta[starts-with(@name, "article_date_original")]/@content',
    '//meta[starts-with(@name, "og:time")]/@content',
    '//meta[starts-with(@name, "apub:time")]/@content',
    '//meta[starts-with(@name, "publication_date")]/@content',
    '//meta[starts-with(@name, "sailthru.date")]/@content',
    '//meta[starts-with(@name, "PublishDate")]/@content',
    '//meta[starts-with(@name, "publishdate")]/@content',
    '//meta[starts-with(@name, "PubDate")]/@content',
    '//meta[starts-with(@name, "pubtime")]/@content',
    '//meta[starts-with(@name, "_pubtime")]/@content',
    '//meta[starts-with(@name, "weibo: article:create_at")]/@content',
    '//meta[starts-with(@pubdate, "pubdate")]/@content',
    '//meta[starts-with(@name, "date")]/@content',
    '//meta[starts-with(@name, "DC.date")]/@content',
]

# 满足下面的XPath，极有可能是文章详情页
ARTICLE_XPATH = [
    '//*[@class="article__content"]',
]
