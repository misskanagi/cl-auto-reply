#!/usr/bin/python
# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
import sys
import re
import time
import random
import logging
import requests
import urllib2
import login_info

from flask import Flask
from google.appengine.api import urlfetch
app = Flask(__name__)
app.config['DEBUG'] = True

def success(val): return val,None
def error(why): return None,why
def get_val(m_val): return m_val[0]
def get_error(m_val): return m_val[1]

encode = 'gbk'
retry_times = 5
replies = [
    '1024',
    u'\u611f\u8c22\u5206\u4eab',
    u'\u8c22\u8c22\u5206\u4eab',
    u'\u611f\u8c22\u697c\u4e3b\u5206\u4eab',
    u'\u611f\u8c22\u5206\u4eab\uff5e'
]

def fetchPageHtml(url):
    retry = 0
    while True:
        try:
            session = requests.session()
            response = session.get(url)
            if response.status_code != 200:
                return error("Failed to fetch html. CODE:%i" % response.status_code)
            elif (response.text) == 0:
                return error("Empty html.")
            else:
                if encode != None:
                    response.encoding = encode
                #print(response.encoding)
                #print(response.text)
                return success(response.text)
        except requests.ConnectionError:
            if retry<retry_times:
                retry+=1
                continue
            global has_log_file
            return error("The server is not responding.")

def reply(session, url, title, content):
    payload = {
        'action' : 'reply',
        'article' : '',
        'atc_attachment' : 'none',
        'atc_autourl' : '1',
        'atc_content' : content.encode('gbk'),
        'atc_convert' : '1',
        'atc_title' : ('Re:'+title).encode('gbk'),
        'atc_usesign' : '1',
        'fid' : '8',
        'pid' : '',
        'step' : '2',
        'tid' : url.split('.')[-2].split('/')[-1],
        'verify' : 'verify'
    }
    headers = {
        'Referer' : url,
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0)like Gecko',
    }
    time.sleep(2)
    response = session.post("http://t66y.com/post.php?", data=payload, headers=headers)
    response.encoding = encode
    return success(0)
    """"
    prog = re.compile(u'\u767c\u8cbc\u5b8c\u7562\u9ede\u64ca\u9032\u5165\u4e3b\u984c\u5217\u8868', re.IGNORECASE)
    matches = prog.findall(unicode(response.text))
    if len(matches)==0:
        res = checkIfReachLimit(response.text)
        if not get_error(res):
            return error(1)
        else:
            res = checkIfTimeLimit(response.text)
            if not get_error(res):
                return error(2)
        return error(3)
    else:
        return success(0)
    """

def checkIfReachLimit(html):
    prog = re.compile(u'\u4f60\u6240\u5c6c\u7684\u7528\u6236\u7d44\u6bcf\u65e5\u6700\u591a\u80fd\u767c\s*([0-9]+?)\s*\u7bc7\u5e16\u5b50', re.IGNORECASE)
    matches = prog.findall(html)
    if len(matches) == 0:
        return error('no')
    else:
        return success(matches[0])

def checkIfTimeLimit(html):
    prog = re.compile(u'\u704c\u6c34\u9810\u9632\u6a5f\u5236\u5df2\u7d93\u6253\u958b\uff0c\u57281024\u79d2\u5167\u4e0d\u80fd\u767c\u8cbc', re.IGNORECASE)
    matches = prog.findall(html)
    if len(matches) == 0:
        return error('no')
    else:
        return success(matches[0])

def login(username, password):
    session = requests.session()
    # get cookies first
    r = session.get('http://t66y.com/login.php')
    time.sleep(2)
    payload = {
        'cktime' : '2592000',
        'forward' : 'http://t66y.com/index.php',
        'hideid' : '0',
        'jumpurl' : 'http://t66y.com/index.php',
        'pwpwd' : password,
        'pwuser' : username,
        'step' : '2'
    }
    headers = {
        'Referer' : 'http://t66y.com/login.php',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0)like Gecko',
    }
    session.cookies = r.cookies
    response = session.post("http://t66y.com/login.php?", data=payload)
    #print(response)
    response.encoding = encode
    return success(session)
    """
    prog = re.compile(u'\u60a8\u5df2\u7d93\u9806\u5229\u767b\u9304', re.IGNORECASE)
    matches = prog.findall(response.text)
    if len(matches)==0:
        return error('login failed!'+response.text)
    else:
        return success(session)
    """

def fetchRandomThreadUrl():
    time.sleep(2)
    res = fetchPageHtml('http://t66y.com/thread0806.php?fid=8')
    if get_error(res):
        return
    html = get_val(res)
    prog = re.compile(r'<h3><a\s*href\s*=\s*["\']?([^\'">]+?)[ \'"]\s*target="_blank"\s*id=""\s*>(?:<font color=green>)?([^<]*)(?:</font>)?</a></h3>', re.IGNORECASE)
    matches = prog.findall(html)
    rand = int(random.uniform(0, len(matches)))
    target = matches[rand]
    return success(('http://t66y.com/'+target[0], target[1]))

def fetchRandomThreadUrlTest():
    time.sleep(2)
    res = urlfetch.fetch('http://t66y.com/thread0806.php?fid=8')
    html = res.content.decode(encode)
    prog = re.compile(r'<h3><a\s*href\s*=\s*["\']?([^\'">]+?)[ \'"]\s*target="_blank"\s*id=""\s*>(?:<font color=green>)?([^<]*)(?:</font>)?</a></h3>', re.IGNORECASE)
    matches = prog.findall(html)
    rand = int(random.uniform(0, len(matches)))
    target = matches[rand]
    return success(('http://t66y.com/'+target[0], target[1]))
    
def autoreply():
    #login
    res = login(login_info.username, login_info.password)
    if get_error(res):
        return res
    session = get_val(res)
    res = fetchRandomThreadUrlTest()
    urlmatch = get_val(res)
    url = urlmatch[0]
    title = urlmatch[1]
    myreply = replies[int(random.uniform(0, len(replies)))]
    res = reply(session, url, '1024', myreply)
    return success('done!')

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.route('/task/autoreply')
def do_auto_reply():
    reload(sys)
    sys.setdefaultencoding('utf8')
    res = autoreply()
    if get_error(res):
        return get_error(res)
    else:
        return 'done!'

@app.errorhandler(404)
def page_not_found(e):
    #Return a custom 404 error.
    return 'Sorry, nothing at this URL.', 404