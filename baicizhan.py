# coding:utf-8
import urllib.request
import urllib
import re
import os
import http.cookiejar
import shutil # 高效处理文件的模块
from bs4 import BeautifulSoup
import random
import csv

host = 'http://www.baicizhan.com/login'
email = '13560340051'
pwd = ''
data = {'email':email,'raw_pwd': pwd}
post_data = urllib.parse.urlencode(data).encode(encoding='UTF8')
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
response = opener.open(host, post_data)
print(response.read())
