#-*- coding: utf-8 -*-

from urllib import quote_plus as q, unquote_plus as unq, urlencode
from urllib2 import build_opener, urlopen, HTTPCookieProcessor
from cookielib import CookieJar
import urlparse
import re
import urllib
import urllib2
import time
from tqdm import tqdm
__author__ = 'bluele'

BASE_URL = 'https://www.google.co.kr'
BASE_SEARCH_URL = BASE_URL + '/searchbyimage?%s'

REFERER_KEY = 'Referer'

Opener = build_opener(HTTPCookieProcessor(CookieJar()))
Opener.addheaders = [
    ('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'),
    ('Accept-Language','ko,en-us;q=0.7,en;q=0.3')
]

image_url_pattern = re.compile(ur'^http://www.google.co.kr/imgres\?imgurl=(?P<url>[^&]+)')

def get_referer_index():
    i = 0
    for k, v in Opener.addheaders:
        if k == REFERER_KEY:
            return i
        i += 1
    else:
        return None


def get_referer():
    cur = get_referer_index()
    if cur is not None:
        return Opener.addheaders[cur]
    else:
        return None


def set_referer(url):
    cur = get_referer_index()
    if cur is not None:
        del Opener.addheaders[cur]
    Opener.addheaders.append(
        (REFERER_KEY, url)
    )


def search_image(url):
    params = {
        'image_url': url,
        'hl': 'ko',
        }
    query = BASE_SEARCH_URL % urlencode(params)
    f = Opener.open(query)
    url = f.url
    # domain
    # url += '&as_sitesearch=zozo.jp'
    f = Opener.open(url)
    html = f.read()
    set_referer(f.url)
    return html

def imgtostr(url):
    if(len(url)<10):
        return 'aassdd'
    import sys
    #url = 'http://shopping.phinf.naver.net/main_7808758/7808758563.20140714102303.jpg'
    html = search_image(url)
    qq='<a class="_gUb" href="/search?hl=ko&amp;q='
    src=html.find(qq)
    html=html[src+len(qq):]
    qq='&amp;sa='
    dst=html.find(qq)
    html=html[:dst]
    if(len(html)>300):
        html='aassdd'
    return html
    #print html

def main():
    bo = False
    l=open('log', 'r')
    last = l.readline()
    print "restart:", last
    l.close()
    f=open('img.txt','r')
    w=open('out.txt','a')
    datas=f.readlines()
    for data in tqdm(datas):
        flag = data.split('/')[-1].split('.')[0]
        if flag == last:
            bo = True
        if not bo:
            continue
        l = open('log', 'w')
        l.write(flag)
        l.close()
        time.sleep(2)
        try:
            imgdata=imgtostr(data)
        except:
            print "request faile, wait for 3s"
            time.sleep(3)
            try:
                imgdata=imgtostr(data)
            except:
                print "request faile, wait for 5s"
                time.sleep(5)
                imgdata=imgtostr(data)
        i2=""
        if(imgdata!='aassdd'):

            i2= urllib.unquote(imgdata).decode('utf8')


        query=data.strip()
        query+='/**/'
        
        i2=i2.replace('+',' ')
        query+=i2.strip()
       
        w.write(query.encode('ascii','ignore'))
        w.write("\n")
        
    w.close()
    f.close()
if __name__ == '__main__':
    main()
