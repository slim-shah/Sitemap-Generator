from urllib.request import urlopen
from html.parser import HTMLParser

class TitleParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.match = False
        self.title=''

    def handle_starttag(self, tag, attributes):
        self.match = True if tag == 'title' else False
        #print(self.match)

    def handle_data(self, data):
        if self.match:
            self.title = data
            self.match = False
        #print(str(self.title) + ' ' + str(self.match) )

'''
def main():
    #url = "https://thenewboston.com/forum"
    #html_string = str(urlopen(url).read())

    parser = TitleParser()
    
    f = open('crawled.txt','r')
    for line in f:
        line.replace('\n','')
        html_string = str(urlopen(line).read())
        finder = parser.feed(html_string)
        print(parser.title)
'''
