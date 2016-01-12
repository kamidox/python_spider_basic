# -*- coding: utf-8 -*-
import requests
import re
from HTMLParser import HTMLParser


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

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and _attr(attrs, 'class') == 'guwencont2':
            self.in_div = True

        if tag == 'a' and self.in_div:
            self.in_a = True

    def handle_endtag(self, tag):
        if tag == 'div':
            self.in_div = False

        if tag == 'a':
            self.in_a = False

    def handle_data(self, data):
        if self.in_a:
            print(data)
            m = self.pattern.match(data)
            if m: self.tangshi_list.append(m.groups())


def retrive_tangshi_300():
    url = 'http://www.gushiwen.org/gushi/tangshi.aspx'
    r = requests.get(url)
    parser = PoemParser()
    parser.feed(r.content)
    return parser.tangshi_list


if __name__ == '__main__':
    l = retrive_tangshi_300()
    print('total %d poems.' % len(l))
    for i in range(10):
        print('标题: %s\t作者：%s' % (l[i]))

