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
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer,encoding='utf-8')




# menuLists = ['综合电影', '日韩电影', '欧美电影', '国内电影', '最新电影']

menuLists = ['最新电影']


class Dytt(object):

    def __init__(self):
        self._movieInfos = ['.*译　　名', '.*片　　名', '.*豆瓣评分',
                            '.*IMDb评分', '.*类　　别', '.*年　　代', '.*国　　家']
        self._searchurl = 'http://s.dydytt.net/plus/search.php?kwtype=0&searchtype=title&'
        self._host = 'http://www.ygdy8.com/'
        self._filePath = '/Users/tangrubei/movieList.txt'

    def createKey(self,keyword):
        return self._searchurl+urllib.parse.urlencode({'keyword': keyword.encode('gbk')})


    def createSoup(self, url):
        rep = requests.get(url)
        return BeautifulSoup(rep.text.encode(
            'iso-8859-1').decode('gbk', errors="ignore"), 'lxml')

    def getResultHref(self,url):
        soup = self.createSoup(url)
        return list(map(lambda tag:self._host+tag.attrs['href'],soup.find(class_='co_content8').find_all('a')))


    def getMovieInfo(self, url):
        movieInfo = '\n------------------------来自电影天堂------------------------------\n'
        soup = self.createSoup(url)
        for moveItem in self._movieInfos:
            if soup.find(text=re.compile(moveItem)):
                movieInfo += '\n'+soup.find(text=re.compile(moveItem)).replace("\r\n", "").replace(" ", "")
        movieInfo += '\n下载路径'
        for downLink in list(map(lambda tag:tag.text, soup.find_all(href=re.compile(".*ftp:")))):
            movieInfo += '\n'+downLink
        return movieInfo


    def wrifile(self,movieInfo):
        if os.path.exists(self._filePath):
            with open(self._filePath,'a',encoding='utf-8') as f:
                f.write(movieInfo)
        else:
            with open(self._filePath,'w',encoding='utf-8') as f:
                f.write(movieInfo.encode())


    def searchMoive(self,keyword):
        searchUrl = self.createKey(keyword)
        resultHrefs = self.getResultHref(searchUrl)
        for href in resultHrefs:
            print(href)
            # print(self.getMovieInfo(href))
            # self.wrifile(self.getMovieInfo(href))


dytt = Dytt()
dytt.searchMoive('血战钢锯岭')
# print(dytt.getMovieInfo('http://www.ygdy8.com/html/gndy/dyzz/20170213/53251.html'))




# dytt = Dytt(menuList=menuLists)
# print(dytt.getMovieItems('http://www.ygdy8.com/html/gndy/china/index.html'))
# print(dytt.getMovieItems(Dytt(menuList=menuLists)))
# print(dytt.menus)
# print(dytt.getMovieInfo('http://www.dytt8.net/html/gndy/dyzz/20170226/53333.html'))


# rep= requests.get(url='http://www.ygdy8.net/html/gndy/china/index.html')
# soup = BeautifulSoup(rep.text.encode('iso-8859-1').decode('gbk', errors="ignore"), 'lxml')
# soup.find(class_='co_content8')
# bs = soup.findAll('b')
# for b in bs:
#     ahs = b.find_all('a')
#     print(ahs[1].text)
#     print(ahs[1].attrs['href'])
# # print(bs)


# dytt = Dytt(menuList=menuLists)
# print(dytt.getMovieItems('http://www.ygdy8.net/html/gndy/oumei/index.html'))
