#-*- coding:UTF-8 -*-#
import os
import time
import requests
from module_adsl import get_adsl

def adsl():
    try:
        os.system("rasdial ADSL /disconnect")
        os.system("rasdial ADSL " + get_adsl())
        r = requests.get('http://www.sina.com.cn/',timeout=30)
        if(r.status_code==200):
            print 'can be connect'
        else:
            time.sleep(20)
            adsl()
    except:
        print 'adsl connect error'
        adsl()