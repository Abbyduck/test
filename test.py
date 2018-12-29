# coding:utf-8

import urllib.request
import urllib
import re
import os
import shutil # 高效处理文件的模块
from bs4 import BeautifulSoup
import random






#sys为system的缩写，引入此模块是为了改变默认编码 
import sys

#reload(sys)
#sys.setdefaultencoding('utf8')  #设置系统的编码为utf8，便于输入中文
# url = "http://www.dianping.com"

host = 'http://www.dianping.com'
#自定义UA头部，直接用即可，不用理解细节
# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

#user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'
#headers = {'User-Agent':user_agent}
key_word = '沪上阿姨'                                      #写好要搜索的关键词
city_num = str(10)                                     #武汉的城市编码为16，其他城市的编码可以在点评网的URL中找到
directory = city_num   #Windows系统下，创建中文目录名前需要制定编码，这里统一用UTF-8

if os.path.exists(directory):
    shutil.rmtree(directory)
    os.makedirs(directory)  #删除后再创建对应的关键词目录
    print ('delete existed directory successfully')
else:
    os.makedirs(directory)
    print ('create directory successfully')

url = host + '/search/keyword/' + city_num

def getDocument(page):
    my_headers=[
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
                "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
                ]


    randdom_header=random.choice(my_headers)
    page = str(page)
    path_name = directory + '\\page_' + page + '.txt'
    file = open(path_name, 'w+',encoding='utf-8') #创建文件

    #由于要搜索的关键词是中文，所以需要进行转码，这里调用了urllib.pathname2url函数
    real_url = url + '/' + '0_' + urllib.request.pathname2url(key_word) + '/p' + page
    #request = urllib.request.Request(real_url, headers = randdom_header)                               #发送网络请求
    req = urllib.request.Request(real_url)
    req.add_header("User-Agent",randdom_header)
    req.add_header("GET",real_url)
    response = urllib.request.urlopen(req)                                                  #得到网络响应
    #print(response.read())
    document = response.read().decode('utf-8')
    #将网页源码用UTF-8解码
    soup = BeautifulSoup(page, 'html.parser')
    items_name = re.findall(r'data-hippo-type="shop"\stitle="([^"]+)"', document, re.S)  #正则匹配出商家名
    items_address = re.findall(r'<span\sclass="addr">([^\s]+)</span>', document, re.S)   #正则匹配出地址
    items_star = re.findall(r'<span\sclass="sml-rank-stars sml-str([^\s]+)"', document, re.S)   #正则匹配出地址
    items_price = soup.find_all('a', attrs = {'class': 'mean-pricec'})   #正则匹配出地址<a.*class="mean-price"?:.|[\r\n]*<b>([^\s]+)</b>             (?:.|[\r\n])*?

    print(items_price)
    result = ''
    for index in range(len(items_name)):
        result += items_name[index] + '  ' + items_address[index] + '  ' + items_star[index] +'  ' + items_price[index] + '\n'
    file.write(result)                                                                   #将结果存入文件
    file.close()
    print ('Complete!')

def start_crawl2():
    for index in range(0, 2):
        getDocument(index)


start_crawl2()   #开始爬数据！
