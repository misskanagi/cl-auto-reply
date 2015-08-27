from flask import Flask
from google.appengine.api import urlfetch

import re
import time
import random

app = Flask(__name__)
app.config['DEBUG'] = True

encode='gbk'

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

def fetchRandomThreadUrlTest():
    time.sleep(2)
    res = urlfetch.fetch('http://t66y.com/thread0806.php?fid=8')
    html = res.content.decode(encode)
    prog = re.compile(r'<h3><a\s*href\s*=\s*["\']?([^\'">]+?)[ \'"]\s*target="_blank"\s*id=""\s*>(?:<font color=green>)?([^<]*)(?:</font>)?</a></h3>', re.IGNORECASE)
    matches = prog.findall(html)
    rand = int(random.uniform(0, len(matches)))
    target = matches[rand]
    return 'http://t66y.com/'+target[0]

@app.route('/')
def hello():
    #Return a friendly HTTP greeting.
    url = fetchRandomThreadUrlTest()
    res = urlfetch.fetch(url)
    html = res.content.decode(encode)
    return html
    #return 'welcom to cl-auto-reply!'

@app.errorhandler(404)
def page_not_found(e):
    #Return a custom 404 error.
    return 'Sorry, nothing at this URL.', 404
