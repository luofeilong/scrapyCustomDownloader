# encoding: utf-8
__author__ = 'dragon'


import re
from time import time
from cStringIO import StringIO
from urlparse import urldefrag
from zope.interface import implements
from twisted.internet import defer, reactor, protocol
from twisted.web.http_headers import Headers as TxHeaders
from twisted.web.iweb import IBodyProducer
from twisted.internet.error import TimeoutError
from twisted.web.http import PotentialDataLoss
from scrapy.xlib.tx import Agent, ProxyAgent, ResponseDone, HTTPConnectionPool, TCP4ClientEndpoint
from scrapy.http import Headers
from scrapy.responsetypes import responsetypes
from scrapy.core.downloader.webclient import _parse
from scrapy.utils.misc import load_object
from scrapy.http import HtmlResponse
from twisted.internet import utils
from twisted.internet import defer

import spynner
import pyquery
import time
import BeautifulSoup


class MyLogicDownloader(object):
    '''    定制下载逻辑    '''
    def __init__(self, agent=None):
        '''agent: 异步下载代理'''
        self._agent = agent

    def download(self, request):
        '''        需要异步返回，不可以阻塞，本例子的演示直接调用 phantomjs的一个简单包装脚本	'''
        begintime = time.time()
        d = self._download(request)
        d.addCallback(self.parseData, request, begintime)
        print '证明我是异步的'
        return d

    def _download(self, request):
        '''使用twsited 的函数创建异步进程调用'''
        d = utils.getProcessOutput('scrapyweb.js', args=(request.url, '24000'), reactor=reactor)


        def gethtmlpage(request):
            browser = spynner.Browser()
            browser.load(request.url, 80)
            return browser.html

        d = utils.defer()

        d.addCallback(gethtmlpage, request)

        def getOutput(result):
            return result
        d.addCallback(getOutput)
        return d

    def parseData(self, htmldoc, request, begintime):
        '''解析函数，当请求完成后被调用'''
        # 这个下载时间在调整下载速度的扩展 AutoThrottle 中被使用
        request.meta['download_latency'] = time() - begintime
        return HtmlResponse(request.url, body=htmldoc + '\n证明我被解析过', request=request)

class MyDownloadHandler(object):
    '''    下载接口, 被上层所调用    '''
    def __init__(self, settings):
        self._pool = HTTPConnectionPool(reactor, persistent=True)
        self._pool.maxPersistentPerHost = settings.getint('CONCURRENT_REQUESTS_PER_DOMAIN')
        self._pool._factory.noisy = False
        self._contextFactoryClass = load_object(settings['DOWNLOADER_CLIENTCONTEXTFACTORY'])
        self._contextFactory = self._contextFactoryClass()

    def download_request(self, request, spider):
        '''下载的主要被调用接口（异步），返回 deferred (twisted 的延迟回调对象)'''
        myDownloader = MyLogicDownloader()
        return myDownloader.download(request)

    def close(self):
        return self._pool.closeCachedConnections()