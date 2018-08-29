#-*- coding:UTF-8 -*-#
import re
import time
import adsl
import redis
import requests
import threading

redis_conn = redis.StrictRedis(host='127.0.0.1',port='6379')
pipe = redis_conn.pipeline()


def save(txt):
	global Lock
	f = open('neir.txt','a')
	f.write(txt + '\n')
	Lock.acquire()
	f.close()
	Lock.release()

# def requests(url):
# 	while True:

def crawl_step1(city):
	'''访问主目录'''
	url = 'http://www.herostart.com/%s/' % city
	response = requests.get(url).text.encode('utf-8')
	find_url = re.findall(r'<h2><a href="http://www.herostart.com/(.*?).html">(.*?)</a> </h2>',response)
	for each in find_url:
		crawl_step2(each[0],each[1])


def crawl_step2(endid,type_1):
	print type_1,'start...'
	crawl_list = 'huanqiu'
	page = 1
	while True:
		url = 'http://www.herostart.com/%s-pn%s.html' % (endid,page)
		response = requests.get(url).content
		find_url2 = re.findall(r'<li><a href="http://www.herostart.com/gongsi/(.*?)" >',response)
		####ruku###
		for each2 in find_url2:
			txt = '%s|%s' % (each2,type_1)
			pipe.lpush(crawl_list,txt)
		pipe.execute()
		##################
		print str(page),'finish'
		if len(find_url2) < 38:
			break
		else:
			page += 1
		


def crawl_step3(endid2,type_1):
	url = 'http://www.herostart.com/gongsi/%s' % endid2
	response = requests.get(url).text.encode('utf-8')
	find_name = re.search(r'<h1 style="text-indent:10px;color:#666666">(.*?)</h1>',response).group(1)
	try:
		find_tel = re.search(r'">手机：([\s\S]*?)</li>',response).group(1).strip()
	except:
		find_tel = 'NULL'
	try:
		find_tel2 = re.search(r'">电话：([\s\S]*?)</li>',response).group(1).strip()
	except:
		find_tel2 = 'NULL'
	value_list = [find_name,find_tel,find_tel2,url,type_1]
	save('|'.join(value_list))
	print find_name + 'finish'



if __name__ == '__main__':
	for city in ['hangzhou','wuhan']:
		crawl_step1(city)
# crawl_step2('http://www.herostart.com/hangzhou/c-32.html')
# crawl_step3('http://www.herostart.com/gongsi/caqdhqzjx.html','五金')