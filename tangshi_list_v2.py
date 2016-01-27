# -*- coding: utf-8 -*-
import requests
import re
from HTMLParser import HTMLParser

# ugly code to fix UnicodeDecodeError
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def _attr(attrs, attrname):
    for attr in attrs:
        if attr[0] == attrname:
            return attr[1]
    return None


class PoemParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_div = False
        self.in_a = False
        self.pattern = re.compile(r'(.*)\((.*)\)')
        self.tangshi_list = []
        self.current_poem = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and _attr(attrs, 'class') == 'guwencont2':
            self.in_div = True

        if tag == 'a' and self.in_div:
            self.in_a = True
            self.current_poem['url'] = _attr(attrs, 'href')

    def handle_endtag(self, tag):
        if tag == 'div':
            self.in_div = False

        if tag == 'a':
            self.in_a = False

    def handle_data(self, data):
        if self.in_a:
            m = self.pattern.match(data)
            if m:
                self.current_poem['title'] = m.group(1)
                self.current_poem['author'] = m.group(2)
                self.tangshi_list.append(self.current_poem)
                self.current_poem = {}


class PoemContentParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.content = []
        self.in_p = False

    def handle_starttag(self, tag, attrs):
        if tag == 'p' and _attr(attrs, 'align') == 'center':
            self.in_p = True

    def handle_endtag(self, tag):
        if tag == 'p':
            self.in_p = False

    def handle_data(self, data):
        if self.in_p:
            self.content.append(data)


def retrive_tangshi_300():
    url = 'http://www.gushiwen.org/gushi/tangshi.aspx'
    r = requests.get(url)
    parser = PoemParser()
    parser.feed(r.content)
    return parser.tangshi_list


def download_poem(poem):
    r = requests.get('http://www.gushiwen.org' + poem['url'])
    parser = PoemContentParser()
    parser.feed(r.content)
    poem['content'] = '\n'.join(parser.content)


if __name__ == '__main__':
    l = retrive_tangshi_300()
    print('total %d poems.' % len(l))
    for i in range(10):
        print('标题: %(title)s\t作者：%(author)s\tURL: %(url)s' % (l[i]))

    # download each poem
    for i in range(len(l)):
        print('#%d downloading poem from: %s' % (i, l[i]['url']))
        download_poem(l[i])
        print('标题: %(title)s\t作者：%(author)s\n%(content)s' % (l[i]))