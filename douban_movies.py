import urllib2
from HTMLParser import HTMLParser


class MovieParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.movies = []

    def handle_starttag(self, tag, attrs):
        def _attr_value(attrs, key):
            for attr in attrs:
                if attr[0] == key:
                    return attr[1]
            return None

        if tag == 'li' and _attr_value(attrs, 'data-category') == 'nowplaying':
            movie = {}
            movie['title'] = _attr_value(attrs, 'data-title')
            movie['score'] = _attr_value(attrs, 'data-score')
            movie['region'] = _attr_value(attrs, 'data-region')
            movie['director'] = _attr_value(attrs, 'data-director')
            movie['actors'] = _attr_value(attrs, 'data-actors')
            print('%(title)s|%(score)s|%(director)s|%(actors)s' % movie)
            self.movies.append(movie)


def nowplaying_movies(url):
    parser = MovieParser()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'}
    req = urllib2.Request(url, headers=headers)
    parser.feed(urllib2.urlopen(req).read())
    return parser.movies


if __name__ == '__main__':
    url = 'http://movie.douban.com/nowplaying/xiamen/'
    movies = nowplaying_movies(url)

    import json
    print('%s' % json.dumps(movies, sort_keys=True, indent=4, separators=(',', ': ')))
