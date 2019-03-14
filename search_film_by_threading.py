# -*- coding: UTF-8 -*-
import os
import urllib
import urllib2
import requests
import random
import re
import threading
import time
import sys
reload(sys) 
sys.setdefaultencoding('utf8')

class MyThread(threading.Thread):
    def __init__(self,func,args=()):
        super(MyThread,self).__init__()
        self.func = func
        self.args = args
    def run(self):
        self.result = self.func(*self.args)
    def get_result(self):
        try:
            return self.result
        except Exception:
            return None

def get_baidu_url(keywork=''):
	my_headers=[
"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",  
"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
]  
	url = u'https://www.fqsousou.com/s/' + keywork + '.html?t=4'
	randdom_header=random.choice(my_headers)
	print url
	req = urllib2.Request(url)
	req.add_header("User-Agent",randdom_header)
	req.add_header("GET", url)
	response = urllib2.urlopen(req)
	#print response.getcode()
	html = response.read()
	#print html
	reg = re.compile(r'<a href="/resource/(.*?)" target="_blank" title="(.*?)">',re.S)
	contents = re.findall(reg, html)
	#print contents[0][0]
	title = contents[0][1]
	print 'title:' + title

	url_1 = 'https://www.fqsousou.com/resource/' + contents[0][0]
	req = urllib2.Request(url_1)
	req.add_header("User-Agent",randdom_header)
	req.add_header("GET", url_1)
	response = urllib2.urlopen(req)
	html_1 = response.read()
	reg = re.compile(r'<a name=\'downurl\' rel="noreferrer" href="(.*?)" target="_blank" rel',re.S)
	contents = re.findall(reg, html_1)
	#print contents
	if contents == None:
		return 'not found url'
	else:
		return title + ':' + str(contents[0])

if __name__ == '__main__':
	tempList = ['红海行动', '泰囧','大话西游', '逃离地球']
	for i in tempList:
		t = MyThread(get_baidu_url,args=(i,))
		t.start()
		t.join()
		print t.get_result()