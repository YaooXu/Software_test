import sys
import os
import re

result_file = None


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
def compare_file(file1_path, file2_path, tot):
    if file1_path == "" or file2_path == "":
        print(
            '文件路径不能为空：file1_name的路径为：{0}, file2_name的路径为：{1} .'.format(file1_path, file2_path))
        sys.exit()

    with open(file1_path, 'r') as f:
        text1_lines = f.readlines()
    with open(file2_path, 'r') as f:
        text2_lines = f.readlines()

    # 输出是都不同
    diff_output = 0
    to_print = ''

    for line1, line2 in zip(text1_lines, text2_lines):
        # 先output再input
        if line1.startswith('output'):
            # 输出
            if line1 == line2:
                break
            elif 'output = <' in line1 and 'at' in line1:
                # 此时是地址不同 没有意义
                break
            else:
                # 真正的不同输出
                to_print += file1_path + ' ' + line1 + file2_path + ' ' + line2 + '\n'
                diff_output += 1
        elif line1.startswith('input'):
            if line1 == line2:
                # 输入相同 可以打印
                to_print = line1 + '\n' + to_print
            elif 'input = <' in line1 and 'at' in line1:
                # 此时是地址不同 没有意义
                continue

    if diff_output:
        result = open(result_file, 'a+')
        result.write('difference %d\n' % (tot + 1))
        result.write(to_print)
        result.close()

    return diff_output


def get_base_filename(filename: str):
    # 得到没有后缀的文件名
    return os.path.splitext(filename)[0]


def compare_all(test_case_path, versions=['3.3', '3.8']):
    global result_file
    result_file = os.path.join(test_case_path, 'compare_result.txt')
    if os.path.exists(result_file):
        os.remove(result_file)
        print('移除文件 %s' % result_file)

    tot = 0
    for root, dirs, files in os.walk(test_case_path):
        if root.endswith('log'):
            if files:
                test = os.path.dirname(root)
                module_name = os.path.split(test)[-1]
                with open(result_file, 'a+') as f:
                    f.write(module_name + ':\n')

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
                    tot += compare_file(filepath_33, filepath_38, tot)

    print('find ' + str(tot) + ' differences')


if __name__ == "__main__":
    test_case_path = 'tmp'
    versions = ['3.3', '3.8']

    compare_all(test_case_path, versions)
