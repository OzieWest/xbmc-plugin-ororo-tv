__author__ = 'SoraMusoka'

import webapp2, urllib2, urllib, re, json

base_url = 'http://ororo.tv'


class OroroParser:
    @staticmethod
    def get_html(url):
        conn = urllib2.urlopen(urllib2.Request(url + urllib.urlencode({})))
        html = conn.read()
        conn.close()
        return html

    @staticmethod
    def get_categories(html_source):
        return re.compile('<a href="/shows/(.+?)" class="name">(.+?)</a>').findall(html_source.decode('utf-8'))

    @staticmethod
    def get_series(html_source):
        series_links = re.compile('<a href="(.+?)" class="episode" data-href="(.+?)" data-id="(.+?)" data-time="(.+?)">(.+?)</a>').findall(html_source.decode("utf-8"))
        series = []
        for url, data_href, id, time, title in series_links:
            series.append({'id': id, 'title': title})

        return series

    @staticmethod
    def get_episode(html_source):
        webm = re.compile("<source src='(.+?)' type='video/webm'", re.IGNORECASE).findall(html_source.decode("utf-8"))[0]
        mp4 = re.compile("<source src='(.+?)' type='video/mp4'>", re.IGNORECASE).findall(html_source.decode("utf-8"))[0]
        sub = re.compile("label='.+?' src='(.+?)' srclang='.+?'>", re.IGNORECASE).findall(html_source.decode("utf-8"))[0]
        series = {'webm': webm, 'mp4': mp4, 'sub': sub}

        return series

    @staticmethod
    def show_response(name):
        show_page = OroroParser.get_html(base_url + "/shows/" + name)
        shows = OroroParser.get_series(show_page)

        json_response = {
            'count': len(shows),
            'shows': shows
        }

        return json_response

    @staticmethod
    def episode_response(name, episode_id):
        url = base_url + "/shows/" + name + "/videos/" + episode_id
        episode_page = OroroParser.get_html(url)
        json_response = OroroParser.get_episode(episode_page)

        return json_response


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.redirect("http://www.google.com/analytics")


class CatalogPage(webapp2.RequestHandler):
    def get(self):
        base_page = OroroParser.get_html(base_url)
        links = OroroParser.get_categories(base_page)
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
        show_name = self.request.get("name")
        video_id = self.request.get("id")
        if len(show_name) == 0:
            self.redirect("http://www.google.com/analytics")

        self.response.headers['Content-Type'] = 'application/json'
        if len(video_id) == 0:
            result = OroroParser.show_response(show_name)
            self.response.out.write(json.dumps(result))
        else:
            result = OroroParser.episode_response(show_name, video_id)
            self.response.out.write(json.dumps(result))


application = webapp2.WSGIApplication([('/', MainPage), ('/catalog', CatalogPage), ('/show', ShowPage), ], debug=True)