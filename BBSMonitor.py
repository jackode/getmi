__author__ = 'jiankliu'
#!/usr/bin/env python
#-*- coding: utf-8 -*-
from urllib.request import urlopen
import re
import urllib.parse
import time

class BBSMonitor:
    def __init__(self):
        self.fetionParam = [('username','13499999999'),
            ('password','fetionpassword'),
            ('sendto','13499999999')]
        self.fetionUrl = "http://sms.api.bz/fetion.php?" +\
                         urllib.parse.urlencode(self.fetionParam)
        self.newPosts = []
        self.usefulPosts = []
        self.usefulMsgs = []
        self.recentPostId = 0
    def getNewPosts(self):
        pass
    def filtPosts(self):
        self.usefulPosts = []
        for line in self.newPosts:
            if not re.search("(转|出手|出售)", line):
                continue
            if not re.search("((T7|T9|K117)([^\d]+|$)|成都|重庆|南充)", line, re.IGNORECASE):
                continue
            self.usefulPosts.append(line)
    def retrieveMsg(self):
        pass
    def sendsms(self):
        for msg in self.usefulMsgs:
            url = self.fetionUrl + "&" + urllib.parse.urlencode([('message',msg)])
            try:
                urlopen(url)
            except:
                continue
            time.sleep(2)
    def startCheckTicket(self):
        while True:
            self.getNewPosts()
            self.filtPosts()
            self.retrieveMsg()
            self.sendsms()
            time.sleep(10)
class NewsmthMonitor(BBSMonitor):
    def __init__(self):
        BBSMonitor.__init__(self)
    def getNewPosts(self):
        self.newPosts = []
        try:
            board = urlopen('http://www.newsmth.net/bbsdoc.php?board=Ticket')
        except:
            return
        boardCont = board.readlines()
        board.close()
        try:
            boardCont = [bytes.decode(elem, 'gb2312') for elem in boardCont]
        except:
            return


        pattern = r"c.o\((\d+),"
        for line in boardCont:
            m = re.match(pattern, line)
            if not m:
                continue
            id = int(m.group(1))
            if id > self.recentPostId:
                self.newPosts.append(line)
                self.recentPostId = id
                print("recent id: {0}".format(self.recentPostId))

    def retrieveMsg(self):
        self.usefulMsgs = []
        patternId = r"c.o\((\d+),"
        patternContent = r"标 题: (.*)\\n发信站(.*)站内--"
        for post in self.usefulPosts:
            m = re.match(patternId, post)
            if not m:
                continue
            id = m.group(1)
            addr = "http://www.newsmth.net/bbscon.php?bid=833&id=" + id
            try:
                fd = urlopen(addr)
                if not fd:
                    continue
                page = fd.read()
                content = bytes.decode(page, 'gb2312')
            except:
                continue
            m = re.search(patternContent, content)
            if not m:
                continue
            msg = m.group(1) + "\n" + m.group(3);
            self.usefulMsgs.append(msg)
class BdwmMonitor(BBSMonitor):
    def __init__(self):
        BBSMonitor.__init__(self)
    def getNewPosts(self):
        board = urlopen('http://www.bdwm.net/bbs/bbsdoc.php?board=TrafficTicket')
        pass

    def retrieveMsg(self):
        self.usefulMsgs = []
        pass
if __name__ == '__main__':
    smth = NewsmthMonitor()
    smth.startCheckTicket()
