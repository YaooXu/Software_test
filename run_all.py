import os
import sys
from analyzer import get_plugin_file, get_map
import subprocess


def run_with_pys(python_file_path: str, input_file_path: str):
    for python_path in python_pathes:
        cmd_line = 'cat %s | %s %s' % (input_file_path, python_path, python_file_path)
        print(cmd_line)
        # os.system(cmd_line)
        subprocess.Popen(['powershell.exe', cmd_line], stdout=sys.stdout)

def plugin_exit(files):
    flag = 0
    for file in files:
        if file.startswith('plugin'):
            flag = 1
    return flag


if __name__ == '__main__':
    print('loading func')
    get_map('./module_func_class.json')

    # 是否重写插装文件
    over_write = 1

    python_pathes = ['E:\Anaconda\envs\PY37\python.exe',
                     'E:\Anaconda\python.exe']

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
                if file.endswith('.py') and not file.startswith('plugin'):
                    python_file_path = os.path.join(root, file)
                    if plugin_exit(files):
                        # 已存在插装文件
                        plugin_file = get_plugin_file(python_file_path, over_write=over_write)
                    else:
                        plugin_file = get_plugin_file(python_file_path)
                elif file.endswith('.txt'):
                    input_file_path = os.path.join(root, file)

            run_with_pys(plugin_file, input_file_path)
