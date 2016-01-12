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
    # {m,n}/{m,}
    print(re.match(r'ab{2,4}', 'abbbbbb').group())
    print(re.match(r'ab{2,5}', 'ab'))
    print(re.match(r'ab{2,}', 'abbbbbb').group())
    # {m,n} non-greedy
    print(re.match(r'ab{2,4}?', 'abbbbbb').group())

    # 转义字符 \ 用来匹配特殊字符
    print(re.search(r'\$(\d+\.\d+)', 'The price is $9.00').groups())

    # [] 集合
    print(re.search(r'0[xX]([0-9A-Fa-f]+)', 'The hex value is 0xFF03D6').groups())
    print(re.search(r'[0-9]{3}-[0-9]{4}-[0-9]{4}', 'The Phone Number is 138-2231-2398').group())
    print(re.search(r'[0-9\-]+', 'The Phone Number is 138-2231-2398').group())
    # |
    print(re.search(r'([0-9]|-)+', 'The Phone Number is 138-2231-2398').group())


def re_pattern_syntax_meta_char():
    # \number
    print(re.search(r'(.+) \1', 'the the').group())
    print(re.search(r'[0-9]{3}(-[0-9]{4})\1', 'The Phone Number is 138-2231-2398'))
    print(re.search(r'[0-9]{3}(-[0-9]{4})\1', 'The Phone Number is 138-2231-2231').group())

    # \A
    print(re.match(r'\A[Nn]ame:', 'Name: Joey').group())
    print(re.match(r'^[Nn]ame:', 'Name: Joey').group())

    # \d\D
    print(re.search(r'\d{3}-\d{4}-\d{4}', 'The Phone Number is 138-2231-2398').group())
    print(re.search(r'(\D+)\d{3}-\d{4}-\d{4}', 'The Phone Number is 138-2231-2398').groups())

    # \s\S: [ \t\n\r\f\v] \f: 换页 \v: 垂直制表
    print(re.match(r'Name:\s+([a-zA-Z]+)', 'Name: \tJoey').groups())
    print(re.match(r'\S+:\s*(\S+)', 'Name: Joey').groups())

    # \w\W: [a-zA-Z0-9_]
    print(re.match(r'(\w+)(\W+)(\w+)', 'Name: Joey').groups())


def re_pattern_flags():
    # re.DEBUG
    print(re.match(r'(\w+)(\W+)(\w+)', 'Name: Joey', re.DEBUG).groups())

    # re.I/re.IGNORECASE
    print(re.match(r'(name)\W+(\w+)', 'Name: Joey'))
    print(re.match(r'(name)\W+(\w+)', 'Name: Joey', re.IGNORECASE).groups())

    # re.DOTALL
    print(re.match(r'.*', 'abc\ndef').group())
    print(re.match(r'.*', 'abc\ndef', re.DOTALL).group())

    # re.VERBOSE
    a = re.compile(r"""
                   \d +  # the integral part
                   \.    # the decimal point
                   \d *  # some fractional digits""")
    b = re.compile(r"""
                   \d +  # the integral part
                   \.    # the decimal point
                   \d *  # some fractional digits""", re.VERBOSE)
    c = re.compile(r"\d+\.\d*")
    print(a.search('20.5'))
    print(b.search('20.5').group())
    print(c.search('20.5').group())

if __name__ == '__main__':
    re_pattern_flags()
