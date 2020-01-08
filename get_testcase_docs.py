import requests
from bs4 import BeautifulSoup
import os

ignoretags = ['gp', 'go',  'gt']
ignoretags2 = ['gr', 'ne']

def gettext(dir, divs):
    if divs.__len__() == 0:
        return
    directory = dir + 'test' + '.py'
    file = open(directory, 'a')
    try:
        print(directory)
        for prei in range(divs.__len__()):
            # print(prei)
            pre = divs[prei].find('pre')
            spans = pre.contents

            ignoreflag = 0

            for i in range(spans.__len__()):
                # print(i)
                if i == 0:
                    continue

                spanstype = type(spans[i])
                if str(spanstype) == "<class 'bs4.element.NavigableString'>":
                    if spans[i] == '\n':
                        if ignoreflag == 1:
                            ignoreflag = 0
                            continue
                    if ignoreflag == 1:
                        continue
                    file.write(spans[i])
                    # print(spans[i], end = '')
                    continue

                classtag = spans[i].attrs.get('class')
                classstyle = spans[i].attrs.get('style')

                if ignoreflag == 1:
                    continue

                if classtag is None:
                    continue

                if classstyle is not None:
                    if classstyle == 'visibility: visible;':
                        continue

                # print(classtag)
                if i == 1: #非法语句
                    if classtag == ['p']:
                        break
                if classtag[0] in ignoretags:
                    continue
                if classtag[0] in ignoretags2:
                    ignoreflag = 1
                    continue
                text = spans[i].contents[0]
                # print(text, end = '')
                file.write(text)

        file.close()
    except IndexError:
        print('IndexError')
        file.close()
        os.remove(directory)

def gethref():
    response = requests.get(
        "https://docs.python.org/3/library/")
    soup = BeautifulSoup(response.content, 'lxml')
    internals = soup.find_all('a', {'class': 'reference internal'})
    hrefs = []
    for internal in internals:
        hrefs.append('https://docs.python.org/3/library/' + internal['href'])

    return hrefs

def solvehref(url):
    html = url

    responsehref = requests.get(html)
    if responsehref.status_code is not 200:
        return

    dir = './source/docs/' + html.split('/')[-1].split('.')[0] + '/'
    print(dir)

    if not os.path.exists(dir):
        os.makedirs(dir)

    souphref = BeautifulSoup(responsehref.content, 'lxml')

    cnt = 0

    divs = souphref.find_all('div', {'class', 'doctest highlight-default notranslate'})
    if divs.__len__() is not 0:
        cnt += 1
    gettext(dir, divs)

    divs = souphref.find_all('div', {'class', 'highlight-python3 notranslate'})
    if divs.__len__() is not 0:
        cnt += 1
    gettext(dir, divs)

if __name__ == '__main__':

    hrefs = gethref()
    for href in hrefs:
        print(href)
        solvehref(href)

    print('end')
