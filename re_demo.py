# -*- coding: utf-8 -*-
import re


def re_demo():
    # 解析价格
    txt = 'If you purchase more than 100 sets, the price of product A is $9.90.'
    m = re.search(r'\$(\d+\.?\d*)', txt)
    if m:
        print(m.groups())
    # 解析数量和价格
    m = re.search(r'(\d+).*\$(\d+\.?\d*)', txt)
    if m:
        print(m.groups())
    # 增加结果可读性
    m = re.search(r'(?P<quantity>\d+).*\$(?P<price>\d+\.?\d*)', txt)
    if m:
        print(m.groups())
        print(m.group('quantity'))
        print(m.groupdict())

    # search vs. match
    print(re.search('c', 'abcd'))
    print(re.match('c', 'abcd'))
    print(re.search('^c', 'abcd'))
    print(re.match('.*c', 'abcd'))
    m = re.match('(.*)c', 'abcd')
    print(m.group(0), m.group(1))

if __name__ == '__main__':
    re_demo()
