from html.parser import HTMLParser
from urllib import parse


class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url, depth):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()
        self.d = dict()
        self.depth1 = depth
        self.title = ''
        self.match = False

    # When we call HTMLParser feed() this function is called when it encounters an opening tag <a>
    def handle_starttag(self, tag, attrs):

        if tag == 'a':
            for (attribute, value) in attrs:
                #print(str(attribute + ' ' + str(value)))
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    self.links.add(url)
                    self.d[url] = {'title': '', 'depth': self.depth1 + 1, 'priority': 1/(self.depth1 +1), 'last-modified': None}

        if tag == 'title':
            self.match = True

    def handle_data(self, data):
        if self.match:
            self.title = data
            self.match = False


    def page_links(self):
        return self.links,self.d,self.title

    def error(self, message):
        pass
