# -*- coding: utf-8 -*-
import re


def re_demo():
    # 解析价格
    txt = 'If you purchase more than 100 sets, the price of product A is $9.90.'
    # 解析数量和价格: pattern/string/MatchObject
    m = re.search(r'(\d+).*\$(\d+\.?\d*)', txt)
    print(m.groups())


def re_method():
    # search vs. match
    print(re.search('c', 'abcd'))
    print(re.match('c', 'abcd'))
    print(re.search('^c', 'abcd'))
    print(re.match('.*c', 'abcd'))
    m = re.match('(.*)c', 'abcd')
    print(m.group(0), m.group(1))

    # split
    s1 = 'Hello, this is Joey'
    print(re.split(r'\W+', s1))

    # findall
    s1 = 'Hello, this is Joey'
    s2 = 'The first price is $9.90 and the second price is $100'
    print(re.findall(r'\w+', s1))
    print(re.findall(r'\d+', s2))

    # findall vs. search
    print(re.search(r'\d+', s2).group())

    # finditer
    s2 = 'The first price is $9.90 and the second price is $100'
    for m in re.finditer(r'\d+', s2):
        print(m.group())

    # sub
    s2 = 'The first price is $9.90 and the second price is $100'
    print(re.sub(r'\d+', '<number>', s2))
    # subn
    print(re.subn(r'\d+', '<number>', s2))

    # sub with function
    def repl_number(m):
        print(m.group())
        return '<number>'
    print(re.sub(r'\d+', repl_number, s2))


def re_match_object():
    # group
    s1 = 'Joey Huang'
    m = re.match(r'(\w+) (\w+)', s1)
    print(m.group(0, 1, 2))
    # named group
    m = re.match(r'(?P<FirstName>\w+) (?P<LastName>\w+)', s1)
    print(m.group('FirstName', 'LastName'))
    print(m.groupdict())
    print(m.group(0, 1, 2))
    # groups
    print(m.groups())
    # start/end/span
    print(m.start(1), m.end(1))
    print(m.span(1))


def re_pattern_syntax():
    # dot
    print(re.match(r'.*', 'abc\nedf').group())
    print(re.match(r'.*', 'abc\nedf', re.DOTALL).group())

    # caret
    print(re.findall(r'^abc', 'abc\nabc'))
    print(re.findall(r'^abc', 'abc\nabc', re.MULTILINE))

    # $
    print(re.findall(r'abc.$', 'abc1\nabc2'))
    print(re.findall(r'abc.$', 'abc1\nabc2', re.MULTILINE))

    # */+/?
    print(re.match(r'ab*', 'a'))
    print(re.match(r'ab+', 'a'))
    print(re.match(r'ab?', 'a'))

    # greedy/non-greedy
    s = '<H1>title</H1>'
    print(re.match(r'<.*>', s).group())
    print(re.match(r'<.*?>', s).group())

    # {m}
    print(re.match(r'ab{2}', 'abb').group())

if __name__ == '__main__':
    re_pattern_syntax()
