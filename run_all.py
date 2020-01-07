import os
import sys
from analyzer import get_instrument_file, load_json
import subprocess


def run_with_pys(python_file_path: str, input_file_path: str):
    for python_path in python_pathes:
        cmd_line = 'cat %s | %s %s' % (input_file_path, python_path, python_file_path)
        print(cmd_line)
        # os.system(cmd_line)
        subprocess.Popen(['powershell.exe', cmd_line], stdout=sys.stdout)

def instrument_exit(files):
    flag = 0
    for file in files:
        if file.startswith('instrument'):
            flag = 1
    return flag


if __name__ == '__main__':
    print('loading func')
    load_json('./module_func_class.json')

    # 是否重写插装文件
    over_write = 1

    python_pathes = ['python33',
                     'python38']

    # print(sys.version[:3])
    test_case_path = './source/'
    for root, dirs, files in os.walk(test_case_path):
        if root.endswith('log'):
            # 遍历到log文件夹，跳过
            continue
        if files:
            # 该目录有文件
            python_file_path, input_file_path = None, None
            for file in files:
                if file.endswith('.py') and not file.startswith('instrument'):
                    python_file_path = os.path.join(root, file)
                    if instrument_exit(files):
                        # 已存在插装文件
                        instrument_file = get_instrument_file(python_file_path, over_write=over_write)
                    else:
                        instrument_file = get_instrument_file(python_file_path)
                elif file.endswith('.txt'):
                    input_file_path = os.path.join(root, file)

            run_with_pys(instrument_file, input_file_path)
