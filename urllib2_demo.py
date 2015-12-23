# -*- coding: utf-8 -*-
import urllib2
import urllib
import cookielib


def urlopen():
    # 普通请求
    s = urllib2.urlopen('http://blog.kamidox.com')
    print(s.read(100))
    s.close()
    # 超时请求以及错误处理
    try:
        s = urllib2.urlopen('http://blog.kamidox.com/not-exist', timeout=1)
    except urllib2.HTTPError, e:
        print(e)
    else:
        print(s.read(100))
        s.close()


def request():
    # 定制 HTTP 头
    headers = {'User-Agent': 'Mozilla/5.0', 'x-my-header': 'my value'}
    req = urllib2.Request('http://blog.kamidox.com', headers=headers)
    s = urllib2.urlopen(req)
    print(s.read(100))
    s.close()

def request_post_debug():
    # POST
    data = {'username': 'kamidox', 'password': 'xxxxxxxx'}
    # headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'plain/text'}
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request('http://www.douban.com', data=urllib.urlencode(data), headers=headers)
    opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))
    s = opener.open(req)
    print(s.read(100))
    s.close()


def install_debug_opener():
    opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1), urllib2.HTTPSHandler(debuglevel=1))
    urllib2.install_opener(opener)


def handle_cookies():
    cookiejar = cookielib.CookieJar()
    cookie_handler = urllib2.HTTPCookieProcessor(cookiejar=cookiejar)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPHandler(debuglevel=1))
    s = opener.open('http://www.douban.com')
    s.close()

    print('=' * 80)
    print(cookiejar._cookies)
    print('=' * 80)

    s = opener.open('http://www.douban.com')
    s.close()

if __name__ == '__main__':
    # install_debug_opener()
    # urlopen()
    # request()
    # request_post_debug()
    handle_cookies()