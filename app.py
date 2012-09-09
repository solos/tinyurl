#!/usr/bin/python
#coding=utf-8

import bottle
from bottle import request, redirect, template, static_file
import short_url
from hashlib import md5
import kyotocabinet as kvdb
import json

app = bottle.Bottle()

DOMAIN = 'localhost'
PORT=":8080"

@app.route('/')
@app.route('/index.htm')
@app.route('/index.html')
def index():
    return template('index', domain=DOMAIN, port=PORT)

@app.route('/api', method="POST")
def tiny():
    tid_db = kvdb.DB()
    if not tid_db.open("tid_db.kch", kvdb.DB.OWRITER | kvdb.DB.OCREATE):
        result = { 'code': 500, 'message': u'键值数据库错误'}
        return json.dumps(result)

    url = request.forms.get('url').strip()
    if not ( url.startswith('http://') or url.startswith('https://') or \
        url.startswith('ftp://') or url.startswith('mailto:') \
        or url.startswith('data:') or url.startswith('ed2k:')):
        url = 'http://%s' % url

    custom_id = request.forms.get('custom_id').strip()
    result = {}

    if custom_id:
        url_db = kvdb.DB()
        if not url_db.open("url.kch", kvdb.DB.OWRITER | kvdb.DB.OCREATE):
            result = { 'code': 500, 'message': u'键值数据库错误'}
            return json.dumps(result)

        longurl = url_db.get(custom_id)

        if longurl:
            url_db.close()
            result = { 'code': 205, 'message': u'短地址已存在', \
                       'url': longurl, 'tinyurl': custom_id }
            return json.dumps(result)
        else:
            url_db.set(custom_id, url)
            url_db.close()
            tinyurl = "http://%s%s/%s" % (DOMAIN, PORT, custom_id)
            result = { 'code': 200, 'message': u'创建短网址成功', \
                       'url': url, 'tid': custom_id, 'tinyurl': tinyurl }
            return json.dumps(result)

    url_md5 = md5(url).hexdigest()
    tid = tid_db.get(url_md5)

    if tid:
        tid_db.close()
        tinyurl = "http://%s%s/%s" % (DOMAIN, PORT, tid)
        result = { 'code': 205, 'message': u'短地址已存在', 'url': url, \
                   'tid': tid, 'tinyurl': tinyurl }
        return json.dumps(result)
    else:
        url_db = kvdb.DB()
        if not url_db.open("url.kch", kvdb.DB.OWRITER | kvdb.DB.OCREATE):
            result = { 'code': 500, 'message': u'键值数据库错误'}
            return json.dumps(result)

        tid_count = tid_db.count()
        tid = short_url.encode_url(tid_count + 1)
        while ( url_db.get(tid) ):
            tid_count += 1
            tid = short_url.encode_url(tid_count + 1)
        tid_db.set(url_md5, tid)
        url_db.set(tid, url)
        tid_db.close()
        url_db.close()
        tinyurl = "http://%s%s/%s" % (DOMAIN, PORT, tid)
        result = { 'code': 200, 'message': u'短地址创建成功', \
                   'url': url, 'tid': tid, 'tinyurl': tinyurl }
        return json.dumps(result)

@app.route('/api/<tid:re:[a-zA-Z0-9]{5,32}>')
def untiny(tid):
    tid = tid.strip()
    url_db = kvdb.DB()
    if not url_db.open("url.kch", kvdb.DB.OWRITER | kvdb.DB.OCREATE):
        result = { 'code': 500, 'message': u'键值数据库错误' }
        return json.dumps(result)
    url = url_db.get(tid)
    if url:
        url_db.close()
        tinyurl = "http://%s%s/%s" % (DOMAIN, PORT, tid)
        return { 'code': 200, 'message': u'短地址还原成功', \
                 'tid': tid, 'tinyurl': tinyurl, 'longurl': url }
    else:
        url_db.close()
        return { 'code': 206, 'message': u'短地址还原失败', \
                 'tid': tid, 'tinyurl': tinyurl }

@app.route('/<tid:re:[a-zA-Z0-9]{5,32}>')
def redirect_url(tid):
    url_db = kvdb.DB()
    if not url_db.open("url.kch", kvdb.DB.OWRITER | kvdb.DB.OCREATE):
        result = { 'code': 500, 'message': u'键值数据库错误' }
        return json.dumps(result)

    url = url_db.get(tid)
    if url:
        url_db.close()
        redirect(url)
    else:
        url_db.close()
        return u'短网址不存在'

@app.route('/static/<filename>')
def server_static(filename):
    return bottle.static_file(filename, root='./static/')

if __name__ == '__main__':
    bottle.debug(False)
    bottle.run(app, host='localhost', reloader=False, port=int(PORT[1:]))
