__author__ = 'jiankliu'
#coding=utf-8
import urllib, urllib2, cookielib
import StringIO
import gzip
import httplib
import socket

def getpagehtml(pageurl,bianma):
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

user_data = {'user': "ljkang1990@163.com",
             'pwd': "ljkang1990"
}
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode(user_data)
opener.open("https://account.xiaomi.com/pass/serviceLoginAuth", login_data)
response=opener.open("https://account.xiaomi.com/pass/userInfo?userId=72383247")
try:
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        video_webpage = f.read()
    else:
        video_webpage = response.read()
except (urllib2.URLError, httplib.HTTPException, socket.error), err:
    print u'ERROR: unable to download video webpage: %s' % str(err)
print video_webpage.decode('utf-8')
