import sys
import os
import re

# 读取配置文件函数
def read_file(file_name):
    try:
        file_handle = open(file_name, 'r')
        text = file_handle.read().splitlines()  # 读取后以行进行分割
        file_handle.close()
        return text
    except IOError as error:
        print(
            'Read file Error: {0}'.format(error))
        sys.exit()


# 比较两个文件
def compare_file(file1_name, file2_name,a):
    if file1_name == "" or file2_name == "":
        print(
            '文件路径不能为空：file1_name的路径为：{0}, file2_name的路径为：{1} .'.format(file1_name, file2_name))
        sys.exit()
    dirname1, filename1 = os.path.split(file1_name)
    dirname2, filename2 = os.path.split(file2_name)
    text1_lines = read_file(file1_name)
    text2_lines = read_file(file2_name)
    length = len(text1_lines)
    temp = 1
    result = open(result_file, 'a')
    for i in range(length):
        if text1_lines[i] != text2_lines[i]:
            k = str(temp)
            temp = temp + 1
            a=a+1
            # TODO: k 现在每次都是1，改为difference的序号
            pattern = r"output = <"
            matchObj = re.match(pattern, text1_lines[i])
            if matchObj==None:#如果返回结果是none
                result.write('difference %d' % (a) + ' on line %d' % (i) + ':\n')
                result.write(filename1 + ':')
                result.write(text1_lines[i] + '\n')
            else:
                result.close()
                return temp-1
            result.write(filename2 + ':')
            matchObj2 = re.match(pattern, text2_lines[i])
            if matchObj2==None:  # 如果返回结果是none

                result.write(text2_lines[i] + '\n')
            else:
                result.write('output=object')
        result.write('\n')

    result.close()
    return temp - 1


def get_base_filename(filename: str):
    # 得到没有后缀的文件名
    return os.path.splitext(filename)[0]


def compare_all(test_case_path, versions):
    tot = 0
    for root, dirs, files in os.walk(test_case_path):
        if root.endswith('log'):
            if files:
                testcase = root.split("\\")[0].split('/')[-1]
                with open(result_file, 'w') as f:
                    f.write(testcase + ':\n')

                for file in files:
                    base_name = get_base_filename(file)
                    if base_name.endswith(versions[0]):
                        # 通过3.8匹配3.3，如果是3.3则跳过
                        continue
                    filepath_38 = os.path.join(root, file)

                    file33 = base_name[:-3] + versions[0] + '.txt'
                    filepath_33 = os.path.join(root, file33)
                    if not os.path.exists(filepath_33):
                        print('%s 不存在' % filepath_33)
                        continue

                    print(filepath_33, filepath_38, '\n')
                    tot += compare_file(filepath_33, filepath_38,tot)

    print('find ' + str(tot) + ' differences')


if __name__ == "__main__":
    test_case_path = '/Users/ziyantao/PycharmProjects/Software_test1'
    versions = ['3.3', '3.8']
    result_file = os.path.join(test_case_path, 'compare_result.txt')
    compare_all(test_case_path, versions)
