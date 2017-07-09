from lxml import html
import requests

class netflix:
    def __init__(self, content_id):
        try:
            movieID = content_id.split('/')[-1]
            page = requests.get('http://www.allflicks.dk/film/'+movieID)
            self.tree = html.fromstring(page.content)
        except:
            pass
        
    def title(self):
        try:
            title = self.tree.xpath('//div[@id="post-8"]/h1/text()')
            title, app = title[0].split(" - ")
        except:
            title = "N/A"
        return title
