# -*- coding: utf-8 -*-
import requests
import urllib
import os
import threading
import datetime


gImageList = []
gCondition = threading.Condition()


class Consumer(threading.Thread):

    def __init__(self, folder='wallpaper', group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(Consumer, self).__init__(group, target, name, args, kwargs, verbose)
        self.folder = folder

    def run(self):
        global gImageList
        global gCondition

        print('%s started' % threading.current_thread())
        while True:
            gCondition.acquire()
            print('%s: trying to download image. Queue length is %d' % (threading.current_thread(), len(gImageList)))
            while len(gImageList) == 0:
                gCondition.wait()
                print('%s: waken up. Queue length is %d' % (threading.current_thread(), len(gImageList)))
            url = gImageList.pop()
            gCondition.release()

            _download_image_v2(url, self.folder)


class Producer(threading.Thread):
    def run(self):
        global gImageList
        global gCondition

        print('%s started' % threading.current_thread())
        imgs = download_wallpaper_list()

        gCondition.acquire()
        for img in imgs:
            if 'downloadUrl' in img:
                gImageList.append(img['downloadUrl'])
        print('%s: produced %d urls. Left %d urls.' % (threading.current_thread(), len(imgs) - 1, len(gImageList)))
        gCondition.notify_all()
        gCondition.release()


def _download_image(url, folder):
    if not os.path.isdir(folder):
        os.mkdir(folder)

    print('%s: downloading %s' % (threading.current_thread(), url))
    _filename = lambda s: os.path.join(folder, os.path.split(url)[1])
    urllib.urlretrieve(url, _filename(url))
    return _filename(url)


def _download_image_v2(url, folder):
    if not os.path.isdir(folder):
        os.mkdir(folder)

    print('%s: downloading %s' % (threading.current_thread(), url))
    _filename = lambda s: os.path.join(folder, os.path.split(url)[1])
    r = requests.get(url)
    with open(_filename(url), 'wb') as f:
        f.write(r.content)
    return _filename(url)


def download_wallpaper_list():
    url = 'http://image.baidu.com/data/imgs'
    params = {
        'pn': 6,
        'rn': 20,
        'col': '壁纸',
        'tag': '国家地理',
        'tag3': '',
        'width': 1600,
        'height': 900,
        'ic': 0,
        'ie': 'utf8',
        'oe': 'utf-8',
        'image_id': '',
        'fr': 'channel',
        'p': 'channel',
        'from': 1,
        'app': 'img.browse.channel.wallpaper',
        't': '0.016929891658946872'
    }
    s = requests.get(url, params=params)
    imgs = s.json()['imgs']
    print('%s: totally get %d images' % (threading.current_thread(), len(imgs)))
    return imgs


if __name__ == '__main__':
    Producer().start()

    for i in range(2):
        Consumer(folder='wallpaper').start()

