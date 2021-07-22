# webslider from:  ttps://github.com/webslides/webslides
from lxml import etree
import requests
import chardet  # 测试字节的编码格式
import re  # 正则表达式
import datetime  # 日期
import os
import sys
import webbrowser
from bs4 import BeautifulSoup 
from easydict import EasyDict as edict
import subprocess
import time

SSR = subprocess.Popen("data/static/ssr/ShadowsocksR-dotnet4.0.exe")


def get_resource_path(relative_path):  # 取得exe后相关资源绝对路径
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def html_merge(file1, file2):
    f1 = open(file1, 'a+', encoding='utf-8')
    with open(file2, 'r', encoding='utf-8') as f2:
        f1.write('\n')
        for i in f2:
            f1.write(i)


url = "https://rsshub.app/initium/latest/zh-hans"  # 端传媒使用rsshub爬取
headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
    'Connection': 'keep-alive',
    'Referer': 'http://www.baidu.com/'
}
proxies = {
    "http": "http://127.0.0.1:1080",
    "https": "http://127.0.0.1:1080",
}

req = requests.get(url, proxies=proxies)
xml_code = req.content.decode(req.encoding)
# print(chardet.detect(xml_code))  # 测试字节的编码格式
tree = etree.XML(xml_code.encode('utf-8'))  # 不知为啥加了encode就可以了


titles = tree.xpath('//item/title/text()')
dates = tree.xpath('//item/pubDate/text()')
date = tree.xpath('//span[@class = "date"]/text()')
arts = tree.xpath('//item/description/text()')
cats = tree.xpath('//item/category/text()')
# 需添加评论。。。


for i in range(len(dates)):
    tmp = dates[i].split(" ")
    table = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sept": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
    tmp[2] = table[tmp[2]]
    dates[i] = tmp[3] + "/" + tmp[2] + "/" + tmp[1]


Dict = {}
for i in range(len(dates)):
    data = [0, 1, 2]
    data[0] = dates[i]
    data[1] = cats[i]
    data[2] = arts[i]
    Dict[titles[i]] = data

ttitle, tdata = 0, 0
tDict = {}
for title, data in Dict.items():
    today = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("20%y/%m/%d")  # ***********************今天的新闻**************************
    if(data[0] == today):
        tDict[title] = data

for i in range(len(list(tDict.items()))):  # 去掉href等杂文字
    soup = BeautifulSoup(list(tDict.items())[i][1][2], features="lxml")
    for a in soup.findAll('a'):
        del a['href']
        del a['src']
        # print(a)

# for i in range(len(tDict)):
# print(sorted(tDict.values())[0][0])

print(len(list(tDict.items())))

web_file = 'data/報紙.html'
html1 = 'data/static/html/html1.html'
html2 = 'data/static/html/html2.html'
web = (web_file.split("/")[-1])

html_merge(web_file, html1)
'''######################################################################################
myDict = []
# 提取<p>中文字
for i in range(len(list(tDict.items()))):
    pure_text = BeautifulSoup(list(tDict.items())[i][1][2], "lxml").find_all('p')
    pure_text = [sentence.string for sentence in pure_text]
    # print(pure_text[4])
    tempDict = edict({'article': pure_text, 'title': list(tDict.items())[i][0]})
    myDict.append(tempDict)
print()
'''
print(list(tDict.items())[0][1][0])
with open(web_file, 'a', encoding='utf-8') as f:  # 设置文件对象    
    for i in range(len(list(tDict.items()))):      # len(list(tDict.items()))
        f.write('<section class="vertical">') 
        f.write('<div class="wrap size-50">')
        f.write(BeautifulSoup(list(tDict.items())[i][1][2], "lxml").prettify())
        f.write('</div>')
        f.write('</section>')
        # print(list(tDict.items())[i][0])
        # print(list(tDict.items())[i][1][2])


html_merge(web_file, html2)


# if(os.path.exists(web)):
#    os.remove(web)
#os.rename(web_file, web)
print(get_resource_path(web_file))
webbrowser.open_new_tab(get_resource_path(web_file))
time.sleep(360)
SSR.kill()
