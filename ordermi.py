__author__ = 'jiankliu'
#coding=utf-8
import re
import urllib,urllib2,cookielib
import StringIO
import gzip
import httplib
import socket
class xiaobai:
    post_data=""#登陆提交的参数
    def __init__(self):
        '''''初始化类，并建立cookies值'''
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1')]
        urllib2.install_opener(opener)

    def login(self,loginurl,bianma):
        '''''模拟登陆'''
        req = urllib2.Request(loginurl,self.post_data)
        _response = urllib2.urlopen(req)
        _d=_response.read()
        _d =_d.decode(bianma)
        return _d

    def getpagehtml(self,pageurl,bianma):
        '''''获取目标网站任意一个页面的html代码'''
        req2=urllib2.Request(pageurl)
        try:
               response = urllib2.urlopen(req2)
               if response.info().get('Content-Encoding') == 'gzip':
                   buf = StringIO.StringIO(response.read())
                   f = gzip.GzipFile(fileobj=buf)
                   video_webpage = f.read()
               else:
                   video_webpage = req2.read()
        except (urllib2.URLError, httplib.HTTPException, socket.error), err:
            print u'ERROR: unable to download video webpage: %s' % str(err)
        return video_webpage.decode(bianma)
    '''
        _response2=urllib2.urlopen(req2)
        _d2=_response2.read()
        _d2 =_d2.decode(bianma)
        return _d2
    '''

if __name__=="__main__":
    x=xiaobai()
    user_data = {'user': "ljkang1990@163.com",
                 'pwd': "ljkang1990"
    }
    #参递一个post参数
    x.post_data=urllib.urlencode(user_data)
    y=x.login("https://account.xiaomi.com/pass/serviceLoginAuth","utf-8")#登陆
    #获取一个页面的html并输出
    print x.getpagehtml("http://www.xiaomi.com/index.php","utf-8")

