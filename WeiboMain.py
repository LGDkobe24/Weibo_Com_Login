# -*- coding: utf-8 -*-
import urllib2
import cookielib

#import BeautifulSoup
import sys, bs4
#sys.modules['BeautifulSoup'] = bs4

import WeiboEncode
import WeiboSearch
import Crawler
from lxml import etree
import lxml.html.soupparser as sper


class WeiboLogin:
    def __init__(self, user, pwd, enableProxy = False):
        "Initiating WeiboLogin, enableProxy represents the status of proxy, closed default"

        print "Initializing WeiboLogin..."
        self.userName = user
        self.passWord = pwd
        self.enableProxy = enableProxy
        
        self.serverUrl = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.11)"
        #self.serverUrl = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.11)&_=1379834957683"
        self.loginUrl = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)"
        self.postHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'}

    def Login(self):
        "Login progress"  
        self.EnableCookie(self.enableProxy)#Configurate cookie or proxy server
        
        serverTime, nonce, pubkey, rsakv = self.GetServerTime()#First step of login
        postData = WeiboEncode.PostEncode(self.userName, self.passWord, serverTime, nonce, pubkey, rsakv)#Encripy username and password
        print "Post data length:\n", len(postData)

        req = urllib2.Request(self.loginUrl, postData, self.postHeader)
        print "Posting request..."
        result = urllib2.urlopen(req)#Second step of login
        text = result.read()
        try:
            loginUrl = WeiboSearch.sRedirectData(text)#Parse redirect result
	    urllib2.urlopen(loginUrl)
        except:
            print 'Login error!'
            return False
            
        print 'Login func success!'
        return True

    def EnableCookie(self, enableProxy):
    	"Enable cookie & proxy (if needed)."
    
    	cookiejar = cookielib.LWPCookieJar()#setup cookie
    	cookie_support = urllib2.HTTPCookieProcessor(cookiejar)

    	if enableProxy:
    	    proxy_support = urllib2.ProxyHandler({'http':'http://xxxxx.pac'})#use proxy
	    opener = urllib2.build_opener(proxy_support, cookie_support, urllib2.HTTPHandler)
    	    print "Proxy enabled"
    	else:
    	    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)

    	urllib2.install_opener(opener)#Build up corresponding opener to cookie

    def GetServerTime(self):
	"Get server time and nonce, which are used to encode the password"
	print "Getting server time and nonce..."
	serverData = urllib2.urlopen(self.serverUrl).read()#get the web page
	print serverData

	try:
	    serverTime, nonce, pubkey, rsakv = WeiboSearch.sServerData(serverData)#Parse serverTime, nonce etc.
	    return serverTime, nonce, pubkey, rsakv
	except:
	    print 'Get server time & nonce error!'
	    return None

if __name__ == '__main__':
    weiboLogin = WeiboLogin('fuck@sina.com', 'fucksina')#name, password
    Flag = weiboLogin.Login()
    if Flag == True:
	print "Login process successful!"
    
    Content_Stream = urllib2.urlopen('http://weibo.com/PKU?page=1')
    Content = Content_Stream.read()
    tree = etree.HTML(Content)
    NewSubTree = tree.xpath(u"//div[@id='plc_main']")
    NewSubTree[0].xpath("//*")
    new = tree.xpath(u"//script")
    new[14].text
    
    #soup = BeautifulSoup(Content)

    #Crawler.FollowedSearch(content_stream)
    #prettified_soup = soup.prettify()
    #print prettified_soup
    #print "---------------------------------------------"
    #print prettified_soup.decode('gbk').encode('gb2312')
    #print content_stream.read()
