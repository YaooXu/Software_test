
import sys
import os

# 读取配置文件函数
def read_file(file_name):
    try:
        file_handle = open(file_name, 'r')
        text = file_handle.read().splitlines()  # 读取后以行进行分割
        file_handle.close()
        return text
    except IOError as error:
        print
        'Read file Error: {0}'.format(error)
        sys.exit()


# 比较两个文件
def compare_file(file1_name, file2_name):
    if file1_name == "" or file2_name == "":
        print
        '文件路径不能为空：file1_name的路径为：{0}, file2_name的路径为：{1} .'.format(file1_name, file2_name)
        sys.exit()
    dirname1, filename1 = os.path.split('/Users/ziyantao/Downloads/Software_test-master/a.text')
    dirname2, filename2 = os.path.split('/Users/ziyantao/Downloads/Software_test-master/b')
    text1_lines = read_file(file1_name)
    text2_lines = read_file(file2_name)
    length=len(text1_lines)
    temp=1
    for i in range(length):
        if text1_lines[i]!=text2_lines[i]:
             k=str(temp)
             temp=temp+1
             result=open('compare_result.text','a')
             result.write(k)
             result.write(':\n')
             result.write(filename1)
             result.write(':')
             result.write(text1_lines[i])
             result.write('\n')
             result.write(filename2)
             result.write(':')
             result.write(text2_lines[i])
             result.write('\n')
    result.close()

if __name__ == "__main__":
    compare_file(r'/Users/ziyantao/Downloads/Software_test-master/a.text', r'/Users/ziyantao/Downloads/Software_test-master/b')  # 传入两文件的路径


