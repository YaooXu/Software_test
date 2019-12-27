import os
import sys


def run_with_pys(python_file_path: str, input_file_path: str):
    for python_path in python_pathes:
        cmd_line = 'cat %s | %s %s' % (input_file_path, python_path, python_file_path)
        print(cmd_line)
        os.system(cmd_line)


if __name__ == '__main__':
    python_pathes = ['E:\Anaconda\envs\PY37\python.exe', 'E:\Anaconda\python.exe']
    # print(sys.version[:3])
    test_case_path = './testcase'
    for root, dirs, files in os.walk(test_case_path):
        if not dirs:
            python_file_path, input_file_path = None, None
            for file in files:
                if file.endswith('.py'):
                    python_file_path = os.path.join(root, file)
                elif file.endswith('.txt'):
                    input_file_path = os.path.join(root, file)
            run_with_pys(python_file_path, input_file_path)
