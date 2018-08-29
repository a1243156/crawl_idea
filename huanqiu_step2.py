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


def crawl_step3(key):
	key2 = key.split('|')
	endid2,type_1 = key2[0],key2[1]
	url = 'http://www.herostart.com/gongsi/%s' % endid2
	response = requests.get(url).text.encode('utf-8')
	try:
		find_name = re.search(r'<h1 style="text-indent:10px;color:#666666">(.*?)</h1>',response).group(1)
	except:
		redis_conn.lpush('huanqiu',key)
	else:
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


def thread_function():
	threads = []
	for index in range(10):
		key = redis_conn.rpop('huanqiu')
		th = threading.Thread(target=crawl_step3,args=(key,))
		threads.append(th)
	for th in threads:
		th.start()
	for th in threads:
		th.join()



if __name__ == '__main__':
	Lock = threading.Lock()
	while True:
		A = redis_conn.llen('huanqiu')
		if A > 10:
			thread_function()
		elif A > 0 and A <= 10:
			key = redis_conn.rpop('huanqiu')
			crawl_step3(key)
		else:
			break
		adsl.adsl()
		time.sleep(1)
