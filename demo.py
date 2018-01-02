#-*- coding:utf-8 -*-
#########################################################################
# File Name: demo.py
# Author: gxw
# mail: 2414434710@qq.com
# Created Time: 二  1/ 2 11:14:55 2018
#########################################################################
#!/usr/bin/python
from bs4 import BeautifulSoup
import urllib2
import re

url = 'https://2.taobao.com'

request = urllib2.Request(url)
response = urllib2.urlopen(request, timeout=20)

try:
    content = response.read().decode("gb2312", 'ignore')
    content = re.sub("charset=gb2312", "charset=utf-8", content, re.I)
    content = content.encode('utf-8', 'ignore')
except:
    content = response.read()
soup = BeautifulSoup(content, 'html.parser')
# get the phone url
url = 'https:'
url = url + soup.find(text=re.compile(u" 手机")).parent.get('href')
print (url)
