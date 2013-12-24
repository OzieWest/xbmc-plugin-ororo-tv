__author__ = 'SoraMusoka'

import webapp2, urllib2, urllib, re, json

base_url = 'http://ororo.tv'


def get_html(url):
    conn = urllib2.urlopen(urllib2.Request(url + urllib.urlencode({})))
    html = conn.read()
    conn.close()
    return html


def get_categories(html_source):
    return re.compile('<a href="/shows/(.+?)" class="name">(.+?)</a>').findall(html_source.decode('utf-8'))


def get_series(html_source):
    series_links = re.compile('<a href="(.+?)" class="episode" data-href="(.+?)" data-id="(.+?)" data-time="(.+?)">(.+?)</a>').findall(html_source.decode("utf-8"))
    series = []
    for url, data_href, id, time, title in series_links:
        series.append({'id': id, 'title': title})

    return series


def get_episode(html_source):
    webm = re.compile("<source src='(.+?)' type='video/webm'", re.IGNORECASE).findall(html_source.decode("utf-8"))[0]
    mp4 = re.compile("<source src='(.+?)' type='video/mp4'>", re.IGNORECASE).findall(html_source.decode("utf-8"))[0]
    sub = re.compile("label='(.+?)' src='(.+?)'", re.IGNORECASE).findall(html_source.decode("utf-8"))
    series = {'webm': webm, 'mp4': mp4, 'sub': sub}

    return series


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("REDIRECT")


class CatalogPage(webapp2.RequestHandler):
    def get(self):
        base_page = get_html(base_url)
        links = get_categories(base_page)
        shows = []
        for url, title in links:
            shows.append({'url': url, 'title': title})

        json_response = {
            'count': len(shows),
            'shows': shows
        }
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(json_response))


class ShowPage(webapp2.RequestHandler):
    def get(self):
        show_url = self.request.get("name")
        show_page = get_html(base_url + "/shows/" + show_url)
        shows = get_series(show_page)

        json_response = {
            'count': len(shows),
            'shows': shows
        }
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(json_response))


class EpisodePage(webapp2.RequestHandler):
    def get(self):
        show_name = self.request.get("name")
        video_id = self.request.get("id")
        url = base_url + "/shows/" + show_name + "/videos/" + video_id
        episode_page = get_html(url)
        json_response = get_episode(episode_page)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(json_response))


application = webapp2.WSGIApplication([('/', MainPage), ('/catalog', CatalogPage), ('/show', ShowPage), ('/episode', EpisodePage), ], debug=True)