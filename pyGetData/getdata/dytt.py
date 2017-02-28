# -*- coding: utf-8 -*-
import sys
import io
import requests
from bs4 import BeautifulSoup
import re
import urllib
import os


if(sys.stdout.encoding != 'utf-8'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

if(sys.stdin.encoding != 'utf-8'):
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

menuLists = ['最新电影']

class Dytt(object):

    def __init__(self):
        self._movieInfos = ['.*译　　名', '.*片　　名', '.*豆瓣评分',
                            '.*IMDb评分', '.*类　　别', '.*年　　代', '.*国　　家']
        self._searchurl = 'http://s.dydytt.net/plus/search.php?kwtype=0&searchtype=title&'
        self._host = 'http://www.ygdy8.com/'
        self._filePath = '/Users/tangrubei/movieList.txt'

    def createKey(self, keyword):
        return self._searchurl + urllib.parse.urlencode({'keyword': keyword.encode('gbk')})

    def createSoup(self, url):
        rep = requests.get(url)
        return BeautifulSoup(rep.text.encode(
            rep.encoding).decode('gbk', errors="ignore"), 'lxml')

    def getResultHref(self, url):
        soup = self.createSoup(url)
        hrefs = list(filter(lambda tag: not tag.has_attr('target'),
                            soup.find(class_='co_content8').find_all('a')))
        return list(map(lambda tag: self._host + tag.attrs['href'], hrefs))

    def getMovieInfo(self, url):
        movieInfo = '\n------------------------来自电影天堂------------------------------\n'
        soup = self.createSoup(url)
        for moveItem in self._movieInfos:
            if soup.find(text=re.compile(moveItem)):
                movieInfo += '\n' + \
                    soup.find(text=re.compile(moveItem)).replace(
                        "\r\n", "").replace(" ", "")
        movieInfo += '\n下载路径'
        for downLink in list(map(lambda tag: tag.text, soup.find_all(href=re.compile(".*ftp:")))):
            movieInfo += '\n' + downLink
        return movieInfo

    def wrifile(self, movieInfo):
        if os.path.exists(self._filePath):
            with open(self._filePath, 'a', encoding='utf-8') as f:
                f.write(movieInfo)
        else:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.write(movieInfo.encode())

    def searchMoive(self, keyword):
        searchUrl = self.createKey(keyword)
        resultHrefs = self.getResultHref(searchUrl)
        for href in resultHrefs:
            print(self.getMovieInfo(href))


dytt = Dytt()
dytt.searchMoive('血战钢锯岭')
