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


# http://www.mr-zx.com
def get_news():
	my_headers=[
"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",  
"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
]  
	url = 'http://www.mr-zx.com/news/'
	randdom_header = random.choice(my_headers)
	print url
	req = urllib2.Request(url)
	req.add_header("User-Agent",randdom_header)
	req.add_header("GET", url)
	response = urllib2.urlopen(req)
	#print response.getcode()
	html = response.read()
	#print html
	#reg = re.compile(r'<div class="tt_title"><a href="(.*?)" target="_blank">(.*?)</a></div>',re.S)
	reg = re.compile(r'<li><a href="(.*?)" target="_blank">(.*?)</a></li>',re.S)
	results = re.findall(reg, html)
	for new in results:
		print 'title:' + new[1] + ":" + new[0]


if __name__ == '__main__':
	get_news()