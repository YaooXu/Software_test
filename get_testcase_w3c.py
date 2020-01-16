import requests
from bs4 import BeautifulSoup
import os

url = 'https://www.w3schools.com/python/python_examples.asp'
test_temp = 'https://www.w3schools.com/python/'
filepath = './source/w3c/'

def gettest():

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    divs = soup.find_all('div', {'class', 'w3-bar-block'})
    for divsi in range(3, divs.__len__()):  # 第一个是下标为3的div
        print(divsi)
        divhrefs = divs[divsi].find_all('a')
        for hrefi in range(divhrefs.__len__()):
            href = divhrefs[hrefi].get('href')
            judge = href.split('?')[0]
            if judge != 'showpython.asp':
                continue
            filename = href.split('=')[-1]
            test_url = test_temp + href
            test_response = requests.get(test_url)
            if test_response.status_code != 200:
                continue
            test_soup = BeautifulSoup(test_response.content, 'lxml')
            test = test_soup.find('textarea')
            if test is None:
                continue
            text = test.contents[0]
            text = text.replace('\r', '')
            dir = filepath + '\\' + filename + '.py'
            file = open(dir, 'w')
            file.write(text)
            file.close()

if __name__ == '__main__':
    gettest()
