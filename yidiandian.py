# coding:utf-8
import urllib.request
import urllib
import re
import os
import shutil # 高效处理文件的模块
from bs4 import BeautifulSoup
import random
import csv

host = 'http://www.dianping.com'
key_word = '一点点'                                      #写好要搜索的关键词
city_num = str(4)                                     #武汉的城市编码为16，广州 4 ，其他城市的编码可以在点评网的URL中找到
directory = 'result'   #Windows系统下，创建中文目录名前需要制定编码，这里统一用UTF-8
result_file= 'yidiandian.csv'

if  not os.path.exists(directory):
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



    #由于要搜索的关键词是中文，所以需要进行转码，这里调用了urllib.pathname2url函数
    real_url = url + '/' + '0_' + urllib.request.pathname2url(key_word) + '/p' + page
    header = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding":"utf-8",
        "Accept-Language":"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
        "Connection":"keep-alive",
        "Host":"www.dianping.com",
        "Referer":real_url,
        "User-Agent":randdom_header,
        'Cookie':"_lxsdk_cuid=16595796581c8-0866c44393244-9393265-1fa400-16595796582c8; _lxsdk=16595796581c8-0866c44393244-9393265-1fa400-16595796582c8; _hc.v=e3b347fc-2332-8a81-48ea-d173148dee38.1535811086; s_ViewType=10; cy=4; cye=guangzhou; _lxsdk_s=%7C%7C0"
        }
    req = urllib.request.Request(real_url,headers=header)
    # req.add_header("User-Agent",randdom_header)
    # req.add_header("GET",real_url)
    response = urllib.request.urlopen(req)                                                  #得到网络响应
    #print(response.read())
    document = response.read().decode('utf-8')
    #print(response.read())
    # htmlf=open('page/p'+page+'.html','r',encoding="utf-8")
    # document=htmlf.read()
    #将网页源码用UTF-8解码
    soup = BeautifulSoup(document, 'html.parser')
    items_name = re.findall(r'data-hippo-type="shop"\stitle="([^"]+)"', document, re.S)  #正则匹配出商家名
    items_address = re.findall(r'<span\sclass="addr">([^\s]+)</span>', document, re.S)   #正则匹配出地址
    items_star = re.findall(r'<span\sclass="sml-rank-stars sml-str([^\s]+)"', document, re.S)   #正则匹配出星级
    tmp_price = soup.find_all('a', attrs = {'class': 'mean-price'})
    items_price=re.findall(r'<a\s.*?>.*?([￥(\d+)|-]+)(?:</b>)*.*?</a>',str(tmp_price),re.S)#正则匹配出价钱
    tmp_review = soup.find_all('a', attrs = {'class': 'review-num'})
    items_review=re.findall(r'<a\s.*?>[\s\S]*?<b>(.*?)</b>',str(tmp_review),re.S) #正则匹配出评论数目
    datas = [items_name,items_address,items_star,items_price,items_review]
    result_csv = []
    for index in range(len(items_name)):
        tmp=[]
        for i in range(0,5):
            tmp.append(datas[i][index])
        result_csv.append(tmp)
    return result_csv




def start_crawl2():
    path_name2 = 'result' + '\\yidiandian.csv'

    result_csv=[]
    for index in range(0, 2):
        result_csv +=getDocument(index)

    print(result_csv)

    with open(path_name2, "w", newline='',encoding='utf-8') as f:
         # with open(birth_weight_file, "w") as f:
        writer = csv.writer(f)
        writer.writerows([['店名','地址','星星','人均','评论数']])
        writer.writerows(result_csv)
        f.close()
    print ('Success!')


start_crawl2()   #开始爬数据！
