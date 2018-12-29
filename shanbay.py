import requests

import random
import json
from bs4 import BeautifulSoup
import re

#模拟浏览器, 扇贝新闻PC端和移动端的阅读模式不同

home = 'https://www.shanbay.com/'
# 登录链接
login_url = 'https://web.shanbay.com/web/account/login'
#login put
login_path = 'https://www.shanbay.com/api/v1/account/login/web/'
# 获得今日单词列表的链接{page}
words_list_url = 'https://www.shanbay.com/api/v1/bdc/library/fresh/?page={}'
# 获得单词details的链接{content_id}
word_detail_url = 'https://www.shanbay.com/bdc/vocabulary/{}/'

header={
    'Accept'    : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control'        : 'max-age=0',
    'Connection' : 'keep-alive',
    'Host' : 'www.shanbay.com',
    'Origin' : 'https://www.shanbay.com',
    'Referer' : 'https://www.shanbay.com/accounts/login/',
    'Upgrade-Insecure-Requests' : '1',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2723.3 Safari/537.36'
             }
def homepage():
    r = requests.get(login_url)
    print(r)

def login(username, password):


    # 创建Session对象,该对象会自动保存cookie信息
    s = requests.Session()
    # 首先获得登录表单的csrftoken,这个在提交用户账号和密码的时候要一起提交
    csrftoken = s.get(login_url).cookies['csrftoken']
    # print(csrftoken)
    login_form_data = {'username': username, 'password': password, 'csrfmiddlewaretoken': csrftoken}
    # s,即session里保存了cookie信息,下面的post之后,s中会添加更多认证信息,包括auth_token,之后用s访问其他页面
    res = s.put(login_path, data=login_form_data, headers=header)
    return s

import pymysql
def link_db():
    db = pymysql.connect(host='localhost',user='root',passwd='mysql',db='vocabulary',port=3306,charset='utf8')
    cursor=db.cursor()

    return cursor


import  time
def get_today_words(username, password):
    s=login(username,password)

    page=1
    words_list = s.get(words_list_url.format(page))
    words_list = json.loads(words_list.text)['data']
    total=words_list['total']
    total_page=total//10
    print('total:'+str(total))
    old_words=[]
    db = pymysql.connect(host='localhost',user='root',passwd='mysql',db='vocabulary',port=3306,charset='utf8')
    cursor=db.cursor()
    words=cursor.execute('select content from words')
    words=cursor.fetchall()

    for word in words:
        old_words.append(word[0])
    cursor.close()
    db.close()

    sql='INSERT INTO `vocabulary`.`words` (`content`, `pronunciation`, `audio`, `cndf`, `endf`, `example`, `shanbay_id`, `dict`) VALUES '

    for page in range(1,total_page+2):
        print(page)
        for word in words_list['objects']:
            if word['content'] in old_words:
                continue
            if(word['content']=='besides'):
                continue
            content=word['content']
            us_audio=word['us_audio']
            pronunciation=word['pronunciation']
            cn_definition=word['definition']
            if 'defn' in word['en_definition'].keys():
                en_definition=word['en_definition']['defn']
            else:
                en_definition=''
            content_id=word['content_id']
            example=''
            detail=crawl_words(content_id)
            if(detail):
                example=detail['example']

            sql += '("'+content+'","'+pronunciation+'","'+us_audio+'","'+cn_definition+'","'+en_definition+'","'+example+'",'+str(content_id)+',1),'
            print(content)
        words_list = s.get(words_list_url.format(page+1))
        words_list = json.loads(words_list.text)['data']


    txtName = "txt/"+time.strftime('%Y%m%d',time.localtime(time.time()))+".txt"
    f=open(txtName, "w",encoding='utf-8')

    f.write(sql)

    f.close()
    print('success!')

def error_log(msg):
    errorfile = "log/"+time.strftime('%Y%m%d',time.localtime(time.time()))+".txt"
    f=open(errorfile, "a")

    f.write(msg+'\n')
    f.close()

def crawl_words(content_id):
    try:
        res=requests.get(word_detail_url.format(content_id))
         #将网页源码用UTF-8解码
        res.encoding='utf-8'
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        #中文翻译
        cn_definition = soup.find_all('div', attrs = {'class': 'cndf'})
        cn_defs=re.findall(r'<span\s.*?>(.*?)</span>',str(cn_definition),re.S)
        cn_def=''
        for index in range(len(cn_defs)):
            cn_def += cn_defs[index] +' '
        #英文解释
        en_definition = soup.find_all('div', attrs = {'id': 'review-definitions'})
        en_def_soup=BeautifulSoup(str(en_definition), 'html.parser')
        en_defs_speech = en_def_soup.find_all('span', attrs = {'class': 'part-of-speech'})
        en_defs = en_def_soup.find_all('span', attrs = {'class': 'content'})
        en_defs_speech=re.findall(r'<span\s.*?>(.*?)</span>',str(en_defs_speech),re.S) #英文词性
        en_defs=re.findall(r'<span\s.*?>(.*?)</span>',str(en_defs),re.S) #英文翻译
        en_def=''
        for index in range(len(en_defs)):
            en_def += en_defs_speech[index]+'. '+ en_defs[index] +'\n'
        #例子
        example = soup.find_all('div', attrs = {'id': 'ex-sys-box'})
        example_soup=BeautifulSoup(str(example), 'html.parser')
        example=example_soup.get_text().replace('  ','').replace('喜欢（0） 不喜欢（0） 更多','').replace('\n','')

        detail={}
        detail['cndf']=cn_def
        detail['endf']=en_def
        detail['example']=example
        return detail
    except Exception as e:
        error_log(str(content_id)+str(e))
        detail={}
        detail['example']=''
        return detail



# crawl_words(5460)
get_today_words('username','pwd')
