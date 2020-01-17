import requests
from bs4 import BeautifulSoup, NavigableString
import os

# gp >>>
# go 输出
# gt ???
ignore_class = ['gp', 'go', 'gt']

ignore_tags2 = ['gr', 'ne']


def check_legal(code: str):
    if code[0] in ['[', '\\', '/', '%', '(', '$']:
        return False

    return True


def gettext(dir, divs):
    file_path = dir + 'test' + '.py'
    file = open(file_path, 'w')
    try:
        print(file_path)
        for prei in range(len(divs)):
            # print(prei)
            pre = divs[prei].find('pre')
            spans = pre.contents
            pre_line_first_tag = None  # 上一行的第一行标签
            trace_back = 0  # 是否是报错的trace back

            for idx, span in enumerate(spans):
                try:
                    if trace_back:
                        # 是报错信息
                        # 有时候是NavigableString 没有clear方法
                        if isinstance(span, NavigableString):
                            # NavigableString中string没法直接编辑
                            span.string.replace_with('')
                        else:
                            span.clear()
                        continue

                    # NavigableString没有class
                    class_type = span.get('class')[0]
                    if class_type in ignore_class:
                        if class_type == 'gp':
                            # >>> 即每一行的开头，故下一个标签就是这一行的开头
                            pre_line_first_tag = spans[idx + 1]
                            # 报错信息结束
                            trace_back = 0
                        elif class_type == 'go' and pre_line_first_tag:
                            # 输出节点需要在上一行补一个Assign
                            if pre_line_first_tag.string.startswith('verbose') or pre_line_first_tag.string.startswith(
                                    'print'):
                                # 存在重复添加verbose?
                                continue
                            pre_line_first_tag.string = 'verbose = ' + pre_line_first_tag.string
                            print('add verbose: ', pre_line_first_tag.string)
                        elif class_type == 'gt':
                            # 此时是报错信息，接下来的需要全部忽略,并把上一行注释掉
                            pre_line_first_tag.string = '# ' + pre_line_first_tag.string
                            #
                            trace_back = 1
                        span.clear()
                except Exception as e:
                    print(e)

            # .text 实际上是用property修饰的get_text
            code_block = pre.text
            if not check_legal(code_block):
                # 不合法的直接跳过
                continue

            code_lines = code_block.split('\n')
            code_lines[-1] = '\n'  # 最后一个本来是'' 转化为换行符

            # for idx, line in enumerate(code_lines):
            #     if line == '':
            #         pass

            print(code_block)
            file.write(code_block)

        file.close()
    except IndexError:
        print('IndexError')
        file.close()
        os.remove(file_path)


def gethref():
    response = requests.get(
        "https://docs.python.org/%s/library/" % VERSION)
    soup = BeautifulSoup(response.content, 'lxml')
    internals = soup.find_all('a', {'class': 'reference internal'})
    hrefs = []
    for internal in internals:
        link = internal['href']
        if '#' in link:
            # 是锚点
            continue
        hrefs.append('https://docs.python.org/%s/library/' % VERSION + link)

    return hrefs


def solvehref(url):
    html = url

    responsehref = requests.get(html)
    if responsehref.status_code is not 200:
        return

    dir = os.path.join(DIR, html.split('/')[-1].split('.')[0] + '/')
    print(dir)

    soup = BeautifulSoup(responsehref.content, 'lxml')

    cnt = 0

    # divs = souphref.find_all('div', {'class', 'doctest highlight-default'})
    # if len(divs) is not 0:
    #     if not os.path.exists(dir):
    #         os.makedirs(dir)
    #     cnt += 1
    #     gettext(dir, divs)

    divs = soup.find_all('div', {'class', 'highlight-python3'})
    if len(divs) is not 0:
        if not os.path.exists(dir):
            os.makedirs(dir)
        cnt += 1
        gettext(dir, divs)


if __name__ == '__main__':
    VERSION = 3.3  # 要爬取的版本信息
    DIR = './tmp/'  # 存放的目录
    hrefs = gethref()
    for href in hrefs[3:]:
        print(href)
        try:
            solvehref(href)
        except:
            pass
    print('end')
