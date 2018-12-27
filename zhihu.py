
# -*- coding: utf-8 -*-)
import urllib2
import requests
import time
from bs4 import BeautifulSoup
import sys
import random
reload(sys) 
sys.setdefaultencoding('utf-8')

import socket
 
_dnscache={}
def _setDNSCache():
    """
    Makes a cached version of socket._getaddrinfo to avoid subsequent DNS requests.
    """
 
    def _getaddrinfo(*args, **kwargs):
        global _dnscache
        if args in _dnscache:
            print str(args)+" in cache"
            return _dnscache[args]
 
        else:
            print str(args)+" not in cache"  
            _dnscache[args] = socket._getaddrinfo(*args, **kwargs)
            return _dnscache[args]
 
    if not hasattr(socket, '_getaddrinfo'):
        socket._getaddrinfo = socket.getaddrinfo
        socket.getaddrinfo = _getaddrinfo
 

def get_article_link(url):
    try:
        #response = urllib2.urlopen(url)
        #res = response.read()
        response = requests.get(url)
        res = response.text
        print res
    except HTTPError as e:
        content = e.read()
        print('exception:',content)
        print('sleep 10s....')
        time.sleep(10)
    pos = res.find('Ark.kindTree = ')
    if( pos != -1):
        pos = pos + len('Ark.kindTree = ')
    pos1 = res.find('Ark.kindIdMap')

    json = res[pos:pos1]
    print json
    #bsObj = BeautifulSoup(res, 'html.parser')
    bsObj = BeautifulSoup(res, 'lxml')
    articles = {}
    kind = {}
    max = 0;
    for link in links:
        l = str(link.get('href'))
        #print 'links:',l
        #print 'urls:',urls
        #print 'type(l):',type(l)
        if( l.find('/category?kind') == 0):
            articles['https://read.douban.com/'+l]='1'
            print l
        if( l.find('/kind/0/') == 0 or l.find('/kind/500/') == 0):
            print '跳过全部:',l
            time.sleep(5);
            continue;
        active_title = ""
        if( l.find('/kind/') == 0):
            print 'l:',l
            for bs in bsObj.find_all('a', {'href':l}, class_='title active'):
                print 'active_kind_title:', bs.text
                active_title = bs.text
                kind['https://read.douban.com'+l] = bs.text
            for bs in bsObj.find_all('a', {'href':l}, class_='title'):
                print 'kind_title:', bs.text
                kind['https://read.douban.com'+l] = bs.text
        if( l.find('https://read.douban.com/column/') == 0):
            articles[l] = active_title
        elif( l.find('?start=') == 0):
            pos = l.find('?start=')
            pos1 = l.find('&', pos)
            if( pos1  != -1):
                start = l[pos+len('?start='):pos1]
                if( int(start) > max):
                    max = int(start)
                print start
                print l

    return articles, max, kind

def get_article(url):

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36' }
        response = requests.get(url, headers = headers)
        response = response.text
    except HTTPError as e:
        content = e.read()
        print('exception:',content)
        print('sleep 10s....')
        time.sleep(10)
        return
    bsObj = BeautifulSoup(response, 'lxml')
    line = ''
    for read in  bsObj.find_all('div', class_='RichContent RichContent--unescapable'):
        line += read.text.encode("utf-8")
        line += '\n'
        
    return line



if __name__ == '__main__':
    print(sys.argv[1])
    body = get_article(sys.argv[1])
    print body

