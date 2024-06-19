# -*- coding: utf-8 -*-

# by wiseflow/bigbrother666sh 2024-06-19
# use llm to extract the html when gne failed
# use openai SDK (openAI servie or any service compiled with openai llm)
# setting the base url and token as you need
# export LLM_API_BASE="https://your-custom-api-base-url.com"
# export LLM_API_KEY="your-service-key"
# highly recommend using **SiliconFlow**'s online inference service for lower costs, faster speeds, and higher free quotas
# Just configure LLM_API_BASE as "https://api.siliconflow.cn/v1"
# Or you may prefer to use my [invitation link](https://cloud.siliconflow.cn?referrer=clx6wrtca00045766ahvexw92), so I can also get more token rewards
# export HTML_PARSE_MODEL="model-to-use-for-this-task"
# highly recommend using alibaba/Qwen2-7B-Instruct/01-ai/Yi-1.5-9B-Chat as the HTML_PARSE_MODEL

from bs4 import BeautifulSoup
from bs4.element import Comment
# pip install json-repair
import json_repair
import os
# pip install openai
from openai import OpenAI


header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/604.1 Edg/112.0.100.0'}


def openai_llm(messages: list, model: str) -> str:
    base_url = os.environ.get('LLM_API_BASE', "")
    token = os.environ.get('LLM_API_KEY', "")

    if token:
        client = OpenAI(api_key=token, base_url=base_url)
    else:
        client = OpenAI(base_url=base_url)

    try:
        response = client.chat.completions.create(messages=messages, model=model, temperature=0.01)

    except Exception as e:
        print(f'openai_llm error: {e}')
        return ''

    print(f'usage:\n {response.usage}')

    return response.choices[0].message.content


def tag_visible(element: Comment) -> bool:
    if element.parent.name in ["style", "script", "head", "title", "meta", "[document]"]:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_soup(soup: BeautifulSoup) -> str:
    res = []
    texts = soup.find_all(string=True)
    visible_texts = filter(tag_visible, texts)
    for v in visible_texts:
        res.append(v)
    text = "\n".join(res)
    return text.strip()


sys_info = '''Your task is to operate as an HTML content extractor, focusing on parsing a provided HTML segment. Your objective is to retrieve the following details directly from the raw text within the HTML, without summarizing or altering the content:

- The document's title
- The complete main content, as it appears in the HTML, comprising all textual elements considered part of the core article body
- The publication time in its original format found within the HTML

Ensure your response fits the following JSON structure, accurately reflecting the extracted data without modification:

```json
{
  "title": "The Document's Exact Title",
  "content": "All the unaltered primary text content from the article",
  "publish_time": "Original Publication Time as per HTML"
}
```

It is essential that your output adheres strictly to this format, with each field filled based on the untouched information extracted directly from the HTML source.'''


async def general_crawler(html: str) -> dict:
    """
    input: html -- html text (same with gne)
    output: result dict - schema same as gne.
    return {} if failed
    """
    model = os.environ.get('HTML_PARSE_MODEL', 'gpt-3.5-turbo')
    soup = BeautifulSoup(html, "html.parser")
    html_text = text_from_soup(soup)
    html_lines = html_text.split('\n')
    html_lines = [line.strip() for line in html_lines if line.strip()]
    html_text = "\n".join(html_lines)

    if len(html_text) > 29999:
        print("content too long for llm parsing, may cause unexpected result")

    messages = [{"role": "system", "content": sys_info}, {"role": "user", "content": html_text}]
    llm_output = openai_llm(messages, model=model)
    result = json_repair.repair_json(llm_output, return_objects=True)

    if not isinstance(result, dict):
        return {}

    if 'title' not in result or 'content' not in result:
        return {}

    # Extract the picture link, it will be empty if it cannot be extracted.
    image_links = []
    images = soup.find_all("img")
    for img in images:
        try:
            image_links.append(img["src"])
        except KeyError:
            continue
    result["images"] = image_links

    # Extract the author information, if it cannot be extracted, it will be empty.
    author_element = soup.find("meta", {"name": "author"})
    if author_element:
        result["author"] = author_element["content"]
    else:
        result["author"] = ""

    return result
