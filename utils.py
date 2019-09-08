import re
from lxml.html import fromstring


def remove_useless_code(html):
    html = re.sub('<style.*?</style ?>', '', html, flags=re.S)
    html = re.sub('<script.*?</script ?>', '', html, flags=re.S)
    html = re.sub('<video.*?</video ?>', '', html, flags=re.S)
    html = re.sub('<iframe.*?</iframe ?>', '', html, flags=re.S)
    html = re.sub('<source.*?</source ?>', '', html, flags=re.S)
    return html


def pre_parse(html):
    html = remove_useless_code(html)
    element = fromstring(html)
    return element


def remove_noise_node(element, noise_xpath_list):
    for noise_xpath in noise_xpath_list:
        nodes = element.xpath(noise_xpath)
        for node in nodes:
            node.getparent().remove(node)
    return element
