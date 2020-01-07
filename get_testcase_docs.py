import requests
from bs4 import BeautifulSoup
import os

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

            for i in range(spans.__len__()):
                # print(i)
                if i == 0:
                    continue

                spanstype = type(spans[i])
                if str(spanstype) == "<class 'bs4.element.NavigableString'>":
                    file.write(spans[i])
                    # print(spans[i])
                    continue

                classtag = spans[i].attrs.get('class')
                # print(classtag)
                if i == 1: #非法语句
                    if classtag == ['p']:
                        break
                if classtag == ['gp'] or classtag == ['go']:
                    continue
                text = spans[i].contents[0]
                # print(text)
                file.write(text)
                # if spans[i].contents is not None:
                #     if classtag == ['gp']:
                #         file.write('\n')
                #     elif classtag == ['go']:
                #         continue
                #     elif classtag == ['kn'] or classtag == ['nn']:
                #         file.write(''.join(spans[i].contents) + ' ')
                #     else:
                #         file.write(''.join(spans[i].contents))

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
