import os

def createCss(project_name):
    path = os.path.join(project_name,'external.css')
    f = open('external.css','r')
    f1 = open(path,'w')
    for line in f:
        f1.write(line)
    f.close()
    f1.close()


def createXml(project_name, crawled_list ,d):
    path1 = os.path.join(project_name, 'sitemap.xml')
    f = open(path1,'w')
    f.write('''<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n''')
    for i in crawled_list:
        i = i.replace('&', '&amp;')
        f.write('<url>\n<loc>' + str(i) + '</loc> \n </url>' )
    f.write("</urlset>")
    f.close()

def createHtml(project_name, crawled_list, d):
    path = os.path.join(project_name, 'crawled.txt')
    path1 = os.path.join(project_name, 'sitemap.html')
    f = open(path1, 'w')
    f.write('''<!DOCTYPE html>\n''')
    f.write('''<html lang="en">
    <head>
    	<meta charset="utf-8" />
    	<title>Table Style</title>
    	<meta name="viewport" content="initial-scale=1.0; maximum-scale=1.0; width=device-width;">
    	<link rel="stylesheet" type="text/css" href="external.css">
    </head>

    <body>
    <div class="table-title">
    <h3>SGP PROJECT - WEB CRAWLER</h3>
    </div>
    <table class="table-fill">
    <thead>
    <tr>
    <th class="text-center">Made By Meet and Keval</th>
    </tr>
    </thead>
    <tbody class="table-hover"> \n''')
    for i in crawled_list:
        f.write('<tr>\n')
        if d[i]['title'] != '':
            f.write('<td class="text-center"><a href="%s">%s</a></td>\n' % (i, d[i]['title']))
        else:
            f.write('<td class="text-center"><a href="%s">%s</a></td>\n' % (i, i))
        f.write('</tr>\n')
    f.write('</tbody>\n</table>\n</body>\n')
    f.write('</html>')
    f.close()

