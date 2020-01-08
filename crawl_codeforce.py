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
# SUBMISSION_URL = 'http://codeforces.com/contest/{ContestId}/submission/{SubmissionId}'
# USER_INFO_URL = 'http://codeforces.com/api/user.status?handle={handle}&from=1&count={count}'

EXT = {'C++': 'cpp', 'C': 'c', 'Java': 'java', 'Python 3': 'py', 'Delphi': 'dpr', 'FPC': 'pas', 'C#': 'cs'}
EXT_keys = EXT.keys()

replacer = {'&quot;': '\"', '&gt;': '>', '&lt;': '<', '&amp;': '&', "&apos;": "'", "&#39;": "'", '<br/>': '\n'}
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

def get_subssion(st, en):
    template = 'http://codeforces.com/problemset/status/page/%s?order=BY_ARRIVED_DESC'
    urls = []

    for i in range(en, st - 1, -1):
        urls.append(template % i)

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        table = soup.find('table', {'class': 'status-frame-datatable'})
        trs = table.find_all('tr')
        show = url.split('/')[6].split('?')[0]
        print(show)

        submissions = []
        for tr_tag in trs[1:]:
            tds = tr_tag.find_all('td')
            link_tag, lang_tag, verdict_tag = tds[0], tds[4], tds[5]

            link = link_tag.find('a').get('href')
            lang = lang_tag.text.strip()
            span = verdict_tag.find('span')
            if span is None:
                continue
            verdict = span.text.strip()
            if lang == "Python 3":
                # print(link, verdict)
                if verdict == "Accepted" or "Happy New Year!":
                    submissions.append(link)
        write_text(submissions)


def get_texturl(url):
    url = 'http://codeforces.com/problemset/submission/50/67642646'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    tb = soup.find('div', {'class': 'datatable'})
    divs = tb.find_all('div')
    texturl = divs[6].contents[5].contents[3].contents[5].find('a').get('href')
    return texturl

def write_text(submissions):
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

        new_directory = 'source' + '/' + 'codeforce_' + str(con_id)
        print(con_id)
        if not os.path.exists(new_directory):
            os.makedirs(new_directory)
        if not os.path.exists(new_directory + '/' + con_id + '.' + ext):
            file = open(new_directory + '/' + con_id + '.' + ext, 'w')
            print(con_id, sub_id)
            file.write(result)
            file.close()
            text = get_testcase(con_id, prob_id)
            file2 = open(new_directory + '/' + 'input.' + "txt", 'w')
            file2.write(text)
            file2.close()


if __name__ == '__main__':

    st, en = eval(input("请输入起始、结束页码："))

    if st > en:
        st, en = en, st

    start_time = time.time()

    get_subssion(st, en)

    end_time = time.time()

    print('Execution time %d seconds' % int(end_time - start_time))
