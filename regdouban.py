__author__ = 'jiankliu'
# -- coding:gbk --
import sys, time, os, re
import urllib, urllib2, cookielib

loginurl = 'https://www.douban.com/accounts/login'
cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

params = {
    "form_email":"your email",
    "form_password":"your password",
    "source":"index_nav" #没有的话登录不成功
}

#从首页提交登录
response=opener.open(loginurl, urllib.urlencode(params))

#验证成功跳转至登录页
if response.geturl() == "https://www.douban.com/accounts/login":
    html=response.read()

    #验证码图片地址
    imgurl=re.search('<img id="captcha_image" src="(.+?)" alt="captcha" class="captcha_image"/>', html)
    if imgurl:
        url=imgurl.group(1)
        #将图片保存至同目录下
        res=urllib.urlretrieve(url, 'v.jpg')
        #获取captcha-id参数
        captcha=re.search('<input type="hidden" name="captcha-id" value="(.+?)"/>' ,html)
        if captcha:
            vcode=raw_input('请输入图片上的验证码：')
            params["captcha-solution"] = vcode
            params["captcha-id"] = captcha.group(1)
            params["user_login"] = "登录"
            #提交验证码验证
            response=opener.open(loginurl, urllib.urlencode(params))
            ''' 登录成功跳转至首页 '''
            if response.geturl() == "http://www.douban.com/":
                print 'login success ! '
                print '准备进行发帖'
                p={"ck":""}
                c = [c.value for c in list(cookie) if c.name == 'ck']
                if len(c) > 0:
                    p["ck"] = c[0].strip('"')

                addtopicurl="http://www.douban.com/group/python/new_topic"
                res=opener.open(addtopicurl)
                html=res.read()

                m= re.search('<input type="hidden" name="topic_id" value="(.+?)">', html)
                p["topic_id"] = m.group(1)
                m= re.search('<input type="hidden" name="topic_id_sig" value="(.+?)">', html)
                p["topic_id_sig"] = m.group(1)
                p["rev_title"] = 'title'
                p["rev_text"] = 'send body'
                p["rev_submit"] = '好了，发言'

                request=urllib2.Request(addtopicurl)
                request.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11")
                request.add_header("Accept-Charset", "GBK,utf-8;q=0.7,*;q=0.3")
                request.add_header("Origin", "http://www.douban.com")
                request.add_header("Referer", "http://www.douban.com/group/python/new_topic")
                opener.open(request, urllib.urlencode(p))

