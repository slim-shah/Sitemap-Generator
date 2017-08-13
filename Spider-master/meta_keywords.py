#stemming is still needed in title rest is okay
from urllib.request import urlopen
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import string
def key_word_extractor(page):
    page = urlopen(page)
    soup = BeautifulSoup(page, "lxml")
    keyword=""
    description=""
    author=""
    Key = list()
    s = set(stopwords.words('english'))
    #Pun = ['?', '/', '-', '_', '#', '$', '.', '(', ')', '%', '@', '!', '^', '*', '=']
    
    for tag in soup.find_all("meta"):
        #print("entered in  for loop ")
    
        if tag.get("name",None) == "description":
            description = tag.get("content",None)

        elif tag.get("name",None) == "keywords":
            keyword =tag.get("content",None)
            #print(keyword)

        elif tag.get("name",None) == "author":
            author=tag.get("content",None)
            #print(author)

    if description =="" and keyword=="" and author=="":
        #print("title true")
        title = str(soup.find("title")).lower()
        title = title.replace("<title>","")
        title = title.replace("</title>","")

        if '/' in title:
            title = title.split('/')[-1]
            
        if '.' in title:
            title = title[:title.index('.')]
        title = "".join(c for c in title if c not in string.punctuation)
        title = list(title.split(' '))
        for i in title:
            if i not in s:
                Key.append(i)
        Key[:] = [ x for x in Key if x!= '' ]
        return Key
    else:
        #print("title false")
        description = description.lower()
        keyword = keyword.lower()
        author = author.lower()
        description = "".join(c for c in description if c not in string.punctuation)
        description.replace(',',' ')
        description = list(description.split(' '))
        for i in description:
            if i not in s:
                Key.append(i)
        keyword = keyword.split(',')
        for i in keyword:
            Key.append(i)
        Key.append(author)
        Key[:] = [x for x in Key if x != '']
        return Key
    
#key_word_extrator("hello")
