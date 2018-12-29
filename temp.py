# -*- coding: utf-8 -*-
"""
Created on Fri May 13 20:13:41 2016
@author: DJ
"""
 
import urllib3
import urllib
import re
import cookielib
import requests
 
class shanbei:
    def __init__(self,username,password):
        
        self.username=username
        self.password=password
        self.cookiejar = cookielib.LWPCookieJar()#LWPCookieJar提供可读写操作的cookie文件,存储cookie对象
        self.cookieSupport= urllib3.HTTPCookieProcessor(self.cookiejar)
        self.opener = urllib3.build_opener(self.cookieSupport, urllib3.HTTPHandler)
        urllib3.install_opener(self.opener)
        self.headerdic={
            'Accept'    : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#            'Accept-Encoding' : 'gzip, deflate',
#            'Accept-Language' : "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2",
            'Cache-Control'        : 'max-age=0',
            'Connection' : 'keep-alive',
#            'Content-Length' : '119',
#            'Content-Type' : 'application/x-www-form-urlencoded',
            'Host' : 'www.shanbay.com',
            'Origin' : 'https://www.shanbay.com',
            'Referer' : 'https://www.shanbay.com/accounts/login/',
            'Upgrade-Insecure-Requests' : '1',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2723.3 Safari/537.36'
             }
             
 
             
    def login(self):
        self.loginURL="https://www.shanbay.com/accounts/login/"
        self.response = self.opener.open(self.loginURL)
        for item in self.cookiejar:
            if item.name=='csrftoken':
                self.scrf=item.value
        self.postdata={'username':self.username,'password':self.password,'csrfmiddlewaretoken':self.scrf}
        postData=urllib.urlencode(self.postdata)
        print self.postdata
        request=urllib3.Request(url=self.loginURL,data=postData,headers=self.headerdic)
        response = self.opener.open(request)
        url = response.geturl()
        text = response.read()
        print url
        f=open(r'H:\shanbeispider\a.txt','w')
        f.write(text)
        print text
            
if __name__=='__main__':
    a=shanbei('用户名','密码')
    a.login()
