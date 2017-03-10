# encode = 'utf-8'
import sys
import io
from bs4 import BeautifulSoup
import requests
import urllib
import os

if(sys.stdout.encoding != 'utf-8'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class Dxbt8(object):

    def __init__(self):
        self._searchurl = 'http://www.btdx8.com/?'
        self._filePath='/Users/tangrubei/movieList.txt'

    def createKey(self, key, value):
        return self._searchurl + urllib.parse.urlencode({key: value.encode('utf-8')})

    def createSoup(self, url):
        rep = requests.get(url)
        return BeautifulSoup(rep.text, 'lxml')

    def getResultHreftargs(self, soup):
        return soup.find_all(class_='entry-thumb lazyload')

    def getMovieInfo(self, targ):
        movieInfo = '\n------------------------来自比特大熊------------------------------\n'
        movieInfo += '名称: ' + targ['title'] + '\n'
        movieInfo += '下载路径:\n' + targ['href'] + '\n'
        return movieInfo

    def searchMoive(self,keyword):
        searchUrl = self.createKey('s',keyword)
        soup = self.createSoup(searchUrl)
        hrefTargs = self.getResultHreftargs(soup)
        for targ in hrefTargs:
            self.wrifile(self.getMovieInfo(targ))


    def wrifile(self, movieInfo):
        print(movieInfo)
        if os.path.exists(self._filePath):
            with open(self._filePath, 'a', encoding='utf-8') as f:
                f.write(movieInfo)
        else:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.write(movieInfo())


dxbt8 = Dxbt8()
searchurl = dxbt8.searchMoive("张三")
# soup = dxbt8.createSoup(searchurl)
# hrefs = dxbt8.getResultHrefs(soup)

# for hef in hrefs:
    # print(hef)
    # print(hef['href'])
    # print(hef['title'])

    #
    # print(rep.text)
