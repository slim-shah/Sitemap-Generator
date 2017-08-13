from urllib.request import urlopen
from link_finder import LinkFinder
from domain import *
from general import *
import hashlib
from title import *
from meta_keywords import *
from bs4 import BeautifulSoup

class Spider:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    dict_file = ''
    queue = set() # maintains set of queue url so it is not added into queue again
    crawled = set() #maintain set of crawled file so it is not crawled again
    d = dict()  #dictionary to maintain data of last modified
    crawled_list = list() #to maintain crawled list in order they are visited
    temp = dict()
    def __init__(self, project_name, base_url, domain_name, D):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.dict_file = Spider.project_name + '/dict.txt'
        Spider.d = D
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            #parser = TitleParser()
            response = urlopen(page_url)


            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url, Spider.d[page_url]['depth'])
            finder.feed(html_string)
            msg = response.read()
            keywords = key_word_extractor(page_url)
            Spider.d[page_url]['keywords'] = keywords
            '''
            if page_url in Spider.d.keys():
                Spider.d[page_url]['keywords'] = keywords
            else:
                Spider.d[page_url]={'title': '', 'depth': 1, 'priority': 0.5, 'last-modified': None}
                Spider.d[page_url]['keywords'] = keywords
            '''

            if 'last-modified' in response.headers:
                Spider.d[page_url]['last-modified']= response.headers['Last-Modified']

            else:
                Spider.d[page_url]['last-modified'] = response.headers['Date']


        except Exception as e:
            print(str(e))
            return set()

        page,d1,Title = finder.page_links()
        Spider.d[page_url]['title'] = Title
        Spider.crawled_list.append(page_url)
        for i in d1:
            if i in Spider.d.keys():
                continue
            else:
                Spider.d[i] = d1[i]
        return page

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name != get_domain_name(url):
                continue

            if (len(Spider.queue) + len(Spider.crawled)) < 30:
                Spider.queue.add(url)


    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
        dict_to_file(Spider.dict_file,Spider.d, Spider.crawled_list)
        #dict_to_file(Spider.dict_file,Spider.d) alternate method

    @staticmethod
    def ReturnValues():
        return Spider.crawled_list, Spider.d


