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
from prettytable import PrettyTable

url = 'https://2.taobao.com'
next_url = url
pre_url = url
arr = []
page = 1

# connec to the server
def connection():
    request = urllib2.Request(url)
    response = urllib2.urlopen(request, timeout=20)

    try:
        content = response.read().decode("gb2312", 'ignore')
        content = re.sub("charset=gb2312", "charset=utf-8", content, re.I)
        content = content.encode('utf-8', 'ignore')
    except:
        content = response.read()
    soup = BeautifulSoup(content, 'html.parser')
    return soup

# show the item
def show():
    table = PrettyTable(["product", "price", "location", "time",  "link"])
    table.align["product"] = "1"
    table.padding_width = 1
    for dic in arr:
        table.add_row([dic['product'], dic['price'], dic['location'], dic['time'], 
             dic['link']])
    print table
    table = PrettyTable(["page"])
    table.add_row([page])
    print table

# get all the item of one page
def get_item(soup):
    for item in soup.find_all("div", "item-info"):
        dic = {'product':'', 'price':'', 'location':'',
                'time':'', 'desc':'', 'link':''}
        # prodect name
        dic['product'] = item.find('img').get('title')
        # price
        dic['price'] = item.find('em').get_text()
        #print (dic['price'])
        # location
        dic['location'] = item.find('div', 'item-location').get_text()
        # time
        dic['time'] = item.find('span', 'item-pub-time').get_text()
        # desc
        # dic['desc'] = item.find('div', 'item-brief-desc').get_text()
        # link
        link = 'https:'
        link = link + item.find('a').get('href')
        dic['link'] = link

        # add to arr
        arr.append(dic)
    if soup.find(text=re.compile(u"上一页")):
        pre_url = 'https:'
        pre_url = pre_url + soup.find(text=re.compile(u"上一页")).parent.get('href')
    if soup.find(text=re.compile(u"下一页")):
        next_url = 'https:'
        next_url = next_url + soup.find(text=re.compile(u"下一页")).parent.get('href')
    show()

# get opt
def opt(flage):
    global page
    global arr
    while flage:
        command = raw_input('>>')
        if command == 'n':
            del arr[:]
            url = next_url
            soup = connection()
            page = page + 1
            get_item(soup)
        elif command == 'p':
            url = pre_url
            if page != 1:
                del arr[:]
                page = page - 1
                soup = connection()
                get_item(soup)
        elif command == 'q':
            break
        else:
            continue

if __name__ == '__main__':
    # get main page
    soup = connection()

    # get the phone url
    url = 'https:'
    url = url + soup.find(text=re.compile(u" 手机")).parent.get('href')
    soup = connection()
    get_item(soup)

    flage = True
    opt(flage)

