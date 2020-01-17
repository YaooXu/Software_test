import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os

def get_testcase(contest_id, problem_id):
    response = requests.get("http://codeforces.com/contest/{Contestid}/problem/{Problemid}".format(Contestid=contest_id, Problemid=problem_id))
    soup = BeautifulSoup(response.content, 'lxml')
    div = soup.find('div', {'class': 'input'})
    brs = div.find('pre')
    text = ""
    for br in brs:
        if str(br) == '<br/>':
            text += "\n"
        else:
            text += str(br)
    if text[0] == '\n':
        text = text[1:]
    return text

if __name__ == '__main__':
    urls = ['http://codeforces.com/problemset/status/1287/problem/B', 'http://codeforces.com/problemset/status/1285/problem/A', 'http://codeforces.com/problemset/status/1288/problem/D']
    url_pre = 'http://codeforces.com'
    dir = './source/codeforce_'

    drive = webdriver.Chrome()

    for conid in range(1,1288):
        for proid in ['A', 'B']:
            url = 'http://codeforces.com/problemset/status/{contestid}/problem/{problemid}'.format(contestid = conid, problemid = proid)
            response = requests.get(url)
            if response.url == 'http://codeforces.com/':
                url = url + str(1)
                proid = proid + str(1)
                # continue

            drive.get(url)
            if conid == 1 and proid == 'A':
                select = drive.find_element_by_name('programTypeForInvoker')
                applybutton = drive.find_element_by_xpath('/html/body/div[5]/div[4]/div[1]/div/div[4]/form/div[5]/input[1]')

                select.send_keys('Python 3')
                applybutton.click()

            soup = BeautifulSoup(drive.page_source, 'lxml')
            trs = soup.find_all('tr')
            if trs[1].find('a') is not None:
                href = url_pre + trs[1].find('a').get('href')
                code_response = requests.get(href)
                code_soup = BeautifulSoup(code_response.content, 'lxml')
                code = code_soup.find('pre').text


                dir_path = dir + str(conid) + str(proid)
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                test_name = str(conid) + str(proid) + '.py'
                test_file = open(dir_path + '/' + test_name, 'w')
                input_file = open(dir_path + '/' + 'input.txt', 'w')
                input_text = get_testcase(conid, proid)
                test_file.write(code)
                input_file.write(input_text)
                input_file.close()
                test_file.close()
                print(str(conid) + str(proid))
            else:
                print('no code')