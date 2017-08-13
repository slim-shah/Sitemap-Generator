import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *
from createSitemap import *


PROJECT_NAME = 'Goose'
HOMEPAGE = 'https://pypi.python.org/pypi/goose-extractor/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
DICT_FILE = PROJECT_NAME + '/dict.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
D = dict()
D[HOMEPAGE] = {'title':PROJECT_NAME,'depth':1,'priority':1,'last-modified':None}
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME, D)


# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


create_workers()
crawl()
print('Spider has finished Crawling')

crawled_list, d = Spider.ReturnValues()
createCss(PROJECT_NAME)
createXml(PROJECT_NAME, crawled_list, d)
createHtml(PROJECT_NAME, crawled_list, d)

print('Sitemap is Generated')

