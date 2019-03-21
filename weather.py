# -*- coding: UTF-8 -*-
import os
import urllib
import urllib2
import requests
import random
import re
import threading
import time
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BlockingScheduler
import sys
reload(sys) 
sys.setdefaultencoding('utf8')


# http://www.mr-zx.com
def get_weather():
	my_headers=[
"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",  
"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
]  
	url = 'http://www.tianqi.com/nanjing/'
	randdom_header = random.choice(my_headers)
	print url
	req = urllib2.Request(url)
	req.add_header("User-Agent",randdom_header)
	req.add_header("GET", url)
	response = urllib2.urlopen(req)
	#print response.getcode()
	html = response.read()
	reg = re.compile(r'<li><a href="/jiangning/" title="(.*?)">',re.S)
	results = re.findall(reg, html)
	if len(results) > 0:
		print results[0]
	return 'NOT_FOUND'



if __name__ == '__main__':
	scheduler = BlockingScheduler()
	#scheduler.add_job(get_news('http://www.tianqi.com/nanjing/'), 'date', run_date='2019-03-18-14:32')
	#scheduler.add_job(get_news, 'interval', seconds=10, id='get_news')
	
	scheduler.add_job(get_news, 'cron', hour = 14,minute = 43,second = 07)
	scheduler.start()
	#url = 'http://www.tianqi.com/nanjing/'
	#get_news(url)