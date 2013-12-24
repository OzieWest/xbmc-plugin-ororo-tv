__author__ = 'SoraMusoka'

import webapp2, urllib2, urllib, re

baseUrl = 'http://ororo.tv'


def get_html(url):
    conn = urllib2.urlopen(urllib2.Request(url + urllib.urlencode({})))
    html = conn.read()
    conn.close()
    return html


def parse_category(html_source):
    return re.compile('<a href="(.+?)" class="name">(.+?)</a>').findall(html_source.decode('utf-8'))


class MainPage(webapp2.RequestHandler):
    def get(self):
        base_page = get_html(baseUrl)
        links = parse_category(base_page)
        for url, title in links:
            self.response.out.write("<a href='" + url + "'>" + title + "</a><br />")


class ShowPage(webapp2.RequestHandler):
    def get(self):
        show_url = self.request.get_all("name")
        self.response.write(show_url)

        #base_page = get_html(show_url)
        #self.response.out.write(base_page)

application = webapp2.WSGIApplication([('/', MainPage), ('/showpage', ShowPage), ], debug=True)