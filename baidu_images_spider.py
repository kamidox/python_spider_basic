# -*- coding: utf-8 -*-
__author__ = 'kamidox@qq.com'

import urllib
import re
import os


def _download_image(url, folder):
    if not os.path.isdir(folder):
        os.mkdir(folder)

    print('downloading %s' % url)
    _filename = lambda s: os.path.join(folder, os.path.split(url)[1])
    urllib.urlretrieve(url, _filename(url))
    return _filename(url)


def main():
    # http://image.baidu.com/channel?c=摄影&t=风景&s=1
    url = 'http://image.baidu.com/channel?c=%E6%91%84%E5%BD%B1&t=%E9%A3%8E%E6%99%AF&s=1'
    s = urllib.urlopen(url)
    data = s.read()

    re_imgs = re.compile(r'.*?"imageUrl"\s*:\s*"(http://.*?)"')
    img_urls = re.findall(re_imgs, data)

    for r in img_urls:
        _download_image(r, 'images')

if __name__ == '__main__':
    main()