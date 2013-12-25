# -*- coding: utf-8 -*-

import sys, urllib, re, urllib2, xbmc, xbmcgui, xbmcplugin, xbmcvfs, xbmcaddon

from os.path import basename
from urlparse import urlsplit

def url2name(url):
    return basename(urlsplit(url)[2])


def download(url, localFileName = None):
    localName = url2name(url)
    req = urllib2.Request(url)
    r = urllib2.urlopen(req)
    if r.info().has_key('Content-Disposition'):
        localName = r.info()['Content-Disposition'].split('filename=')[1]
        if localName[0] == '"' or localName[0] == "'":
            localName = localName[1:-1]
    elif r.url != url: 
        localName = url2name(r.url)
    if localFileName: 
        localName = localFileName
    f = open(localName, 'wb')
    f.write(r.read())
    f.close()


def getHTML(url):
    conn = urllib2.urlopen(urllib2.Request(url + urllib.urlencode({})))
    html = conn.read()
    conn.close()
    return html


def Categories():
    url = 'http://ororo.tv'
    html = getHTML(url)
    genre_links = re.compile('<a href="(.+?)" class="name">(.+?)</a>').findall(html.decode('utf-8'))
    for link, title in genre_links:
        addDir(title, url + link, 20)


def Movies(url):
    html_source = getHTML(url)
    series_links = re.compile('<a href="(.+?)" class="episode" data-href="(.+?)" data-id="(.+?)" data-time="(.+?)">(.+?)</a>').findall(html_source.decode("utf-8").encode('ascii', 'ignore'))
    for episode_url, data_href, episode_id, time, episode_title in series_links:
        addDir(episode_title, 'http://ororo.tv' + data_href, 30)


def Videos(url, title):
    html = getHTML(url)
    videoLink = re.compile("<source src='(.+?)' type='video/mp4'>").findall(html.decode('utf-8'))[0]
    addLink(title + ":video", 'http://ororo.tv' + videoLink)


def get_params():
    param=[]
    paramstring=sys.argv[2]
    print "param string is " + paramstring
    if len(paramstring)>=2:
        print "param bigger than 2"
        params=sys.argv[2]
        cleanedparams=params[1:]
        print "Cleaned params is " + cleanedparams
        if (params[len(params)-1]=='/'):
            print "not sure what this does"
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        print "pair of params" + str(pairsofparams)
        param={}
        for i in range(len(pairsofparams)):
            print "i is " + str(i)
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            print "spilt is " + str(splitparams)
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
            elif (len(splitparams))==3:
                param[splitparams[0]]=splitparams[1]+"="+splitparams[2]
        return param


def addLink(title, url):
    item = xbmcgui.ListItem(title, iconImage='DefaultVideo.png', thumbnailImage='')
    item.setInfo( type='Video', infoLabels={'Title': title} )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=item)


def addDir(title, url, mode):
    sys_url = sys.argv[0] + '?title=' + urllib.quote_plus(title) + '&url=' + urllib.quote_plus(url) + '&mode=' + urllib.quote_plus(str(mode))
    item = xbmcgui.ListItem(title, iconImage='DefaultFolder.png', thumbnailImage='')
    item.setInfo(type='Video', infoLabels={'Title': title})
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys_url, listitem=item, isFolder=True)

params = get_params()
url    = None
title  = None
mode   = None

try:    title = urllib.unquote_plus(params['title'])
except: pass

try:    url = urllib.unquote_plus(params['url'])
except: pass

try:    mode = int(params['mode'])
except: pass

if mode == None:
    Categories()

elif mode == 20:
    Movies(url)

elif mode == 30:
    Videos(url, title)

xbmcplugin.endOfDirectory(int(sys.argv[1]))