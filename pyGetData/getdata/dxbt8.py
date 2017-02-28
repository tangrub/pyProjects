# encode = 'utf-8'
import sys
import io
from bs4 import BeautifulSoup
import requests

if(sys.stdout.encoding != 'utf-8'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class Dxbt8(object):
    def __init__(self):
        pass

rep = requests.get(url='http://www.btdx8.com/?s=%E7%8E%8B%E8%80%85')
soup = BeautifulSoup(rep.text,'lxml')

print("ok")
