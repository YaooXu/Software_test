import urllib.request
import urllib.response
import time, os
import requests
from lxml import etree
from bs4 import BeautifulSoup

MAX_SUBS = 70000000
MAX_CF_CONTEST_ID = 1271
MAGIC_START_POINT = 17000

handle = 'casalazara'

SOURCE_CODE_BEGIN = '<pre id="program-source-text" class="prettyprint lang-py linenums program-source" style="padding: 0.5em;">'
#SUBMISSION_URL = 'http://codeforces.com/contest/{ContestId}/submission/{SubmissionId}'
#USER_INFO_URL = 'http://codeforces.com/api/user.status?handle={handle}&from=1&count={count}'

EXT = {'C++': 'cpp', 'C': 'c', 'Java': 'java', 'Python 3': 'py', 'Delphi': 'dpr', 'FPC': 'pas', 'C#': 'cs'}
EXT_keys = EXT.keys()

replacer = {'&quot;': '\"', '&gt;': '>', '&lt;': '<', '&amp;': '&', "&apos;": "'", "&#39;": "'"}
keys = replacer.keys()


def get_ext(comp_lang):
    if 'Python 3' in comp_lang:
        return 'py'
    for key in EXT_keys:
        if key in comp_lang:
            return EXT[key]
    return ""


def parse(source_code):
    for key in keys:
        source_code = source_code.replace(key, replacer[key])
    return source_code


def get_testcase(contest_id, problem_id):
    # 获取源码
    html = requests.get('http://codeforces.com/contest/{Contestid}/problem/{Problemid}'.format(Contestid=contest_id,
                                                                                               Problemid=problem_id))
    etree_html = etree.HTML(html.text)
    contentinput = etree_html.xpath('//*[@id="pageContent"]/div[2]/div/div/div[5]/div[2]/div[1]//text()')
    if contentinput[0] == 'Input':
        contentinput = contentinput[1:]
    contentoutput = etree_html.xpath('//*[@id="pageContent"]/div[2]/div/div/div[5]/div[2]/div[2]//text()')
    textlist = "".join(contentinput)
    return textlist


def get_subssion(st, en):
    template = 'http://codeforces.com/problemset/status/page/%s?order=BY_ARRIVED_DESC'
    urls = []
    submissions = []
    for i in range(st, en):
        urls.append(template % i)
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        table = soup.find('table', {'class': 'status-frame-datatable'})
        trs = table.find_all('tr')
        for tr_tag in trs[1:]:
            tds = tr_tag.find_all('td')
            link_tag, lang_tag, verdict_tag = tds[0], tds[4], tds[5]

            link = link_tag.find('a').get('href')
            lang = lang_tag.text.strip()
            verdict = verdict_tag.find('span').text.strip()
            if lang == "Python 3":
                # print(link, verdict)
                if verdict == "Accepted":
                    submissions.append(link)
    return submissions

def get_texturl(url):
    url = 'http://codeforces.com/problemset/submission/50/67642646'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    tb = soup.find('div', {'class': 'datatable'})
    divs = tb.find_all('div')
    texturl = divs[6].contents[5].contents[3].contents[5].find('a').get('href')
    return texturl

if __name__ == '__main__':

    st, en = eval(input("请输入起始、结束页码："))

    if st > en:
        st, en = en, st

    start_time = time.time()

    submissions = get_subssion(st, en)

    for submission in submissions:

        submissionurl = 'http://codeforces.com' + submission
        submission_info = urllib.request.urlopen(submissionurl)
        submission_info = submission_info.read().decode('utf-8')
        # print(submission_info)
        start_pos = submission_info.find(SOURCE_CODE_BEGIN, MAGIC_START_POINT) + len(SOURCE_CODE_BEGIN)
        end_pos = submission_info.find("</pre>", start_pos)
        result = parse(submission_info[start_pos:end_pos]).replace('\r', '')
        ext = 'py'

        textlist = submission.split('/')
        con_id = textlist[3]
        sub_id = textlist[4]

        texturl = get_texturl(submissionurl)
        prob_id = texturl.split('/')[4]

        new_directory = 'testcase' + '/' + str(con_id)
        if not os.path.exists(new_directory):
            os.makedirs(new_directory)
        file = open(new_directory + '/' + prob_id + '.' + ext, 'w')
        print(con_id, sub_id)
        file.write(result)
        file.close()
        file2 = open(new_directory + '/' + prob_id + '.' + "txt", 'w')
        file2.write(get_testcase(con_id, prob_id))
        file2.close()

    end_time = time.time()

    print('Execution time %d seconds' % int(end_time - start_time))