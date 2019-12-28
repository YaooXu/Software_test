import os
import re
import ast
import json
import astunparse
import numpy as np

global source, file_parent_path, file_name
cnt = 0
flags = {}


# 测试的时候用的
class v(ast.NodeVisitor):

    def generic_visit(self, node):
        print(type(node).__name__)
        ast.NodeVisitor.generic_visit(self, node)


# 测试的时候用的
class w(v):

    def visit_Load(self, node):
        pass

    def visit_arg(self, node):
        pass

    def visit_argument(self, node):
        pass

    def visit_Call(self, node):
        try:
            print('Call:', node.func.id)
        except:
            print('Call:', node.func.attr)

    def visit_Name(self, node):
        print('Name:', node.id)

    def visit_ClassDef(self, node):
        print('ClassDef:', node.name)
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.FunctionDef):
                print('func name:', sub_node.name)
        print()


# 分析源码的class和method
class SourceAnalyser(ast.NodeVisitor):
    def __init__(self):
        self.all_class = {}
        self.all_func = []
        self.names = set()

    def analyze(self, node):
        self.visit(node)

    def visit_Module(self, node):
        self.generic_visit(node)

    def visit_Name(self, node):
        self.names.add(node.id)

    def visit_FunctionDef(self, node):
        print('func name:', node.name)
        self.all_func.append(node.name)

    def visit_ClassDef(self, node):
        self.all_class[node.name] = []
        print('ClassDef:', node.name)
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.FunctionDef):
                print('method name:', sub_node.name)
                self.all_class[node.name].append(sub_node.name)
        print()


def typeCastToString(castParameter):
    '''
    将任意基本类型的对象转换为字符串
    :param castParameter:需要转换的参数
    '''
    newType = []
    if type(castParameter) == int:
        # 整型转字符串
        newType = str(castParameter)
    elif type(castParameter) == list:
        castParameter_new = []
        for i in castParameter:
            if type(i) == str:
                newType = ','.join(castParameter)
            elif type(i) == int:
                i = str(i)
                castParameter_new.append(i)
                newType = ','.join(castParameter_new)
            elif type(i) == tuple:
                i = ','.join(i)
                castParameter_new.append(i)
                newType = ','.join(castParameter_new)
            elif type(i) == dict:
                i = str(i)
                castParameter_new.append(i)
                newType = ','.join(castParameter_new)

    #     return type(newType)
    return newType


# 分析目标代码的函数调用
class CallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.all_class = {}
        self.names = set()

    def visit_Module(self, node):
        self.generic_visit(node)

    def visit_Name(self, node):
        self.names.add(node.id)

    def visit_ClassDef(self, node):
        # self.all_class[node.name] = []
        # print('ClassDef:', node.name)
        # for sub_node in ast.walk(node):
        #     if isinstance(sub_node, ast.FunctionDef):
        #         print('func name:', sub_node.name)
        #         self.all_class[node.name].append(sub_node.name)
        body = node.body
        for sub_node in body:
            if isinstance(sub_node, ast.FunctionDef):
                self.visit_FunctionDef(sub_node)

        pass

    def visit_FunctionDef(self, node):
        body = node.body
        for sub_node in body:
            if isinstance(sub_node, ast.Assign):
                self.visit_Assign(sub_node)
        pass

    # 判断是否有assign
    def visit_Assign(self, node):
        print("\n------访问Assign节点---")
        line_num = node.lineno

        print("line_num = ", line_num)
        print(source[line_num - 1])
        # print(type(astunparse.dump(node)))
        col_offset = node.col_offset
        if not isinstance(node.value, ast.Call):
            print("节点未调用方法或者函数")
            return

        if 'id' not in node.value.func.__dict__:
            # print('*.*')
            if node.value.func.attr not in flags:
                return
            else:
                print("系统调用：%s" % (node.value.func.attr))
            try:
                global cnt
                # 打log
                log_name = os.path.join(file_parent_path, 'log',
                                        file_name + "_" + str(cnt) + "_line" + str(line_num)
                                        + "_" + node.value.func.value.id + "_" + node.value.func.attr + "_py%s.txt")
                print("log_name = " + log_name)
                # 插入信息
                content = "output =  %s\\n"
                # 插装
                addition = ""
                addition += "%swith open(r\"%s\"%%(sys.version[0:3]), \"w+\", encoding=\'utf8\') as f:\n    %sf.write(\"%s\"%%str(%s))" % (
                    " " * col_offset, log_name, " " * col_offset, content, node.targets[0].id)
                # print(addition)
                source[line_num - 1] += '%s\n' % (addition)
                # print(source[line_num - 1])

                print("插装成功")
                cnt += 1
            except:
                print("错误：节点属性缺少")
        else:
            # print('*')
            if node.value.func.id not in flags:
                print("不是系统调用！")
                return
            else:
                print("系统调用：%s" % (node.value.func.id))
            try:
                # 打log
                log_name = os.path.join(file_parent_path, 'log',
                                        file_name + "_" + str(cnt) + "_line" + str(line_num)
                                        + "_" + node.value.func.id + "_py%s.txt")
                print("log_name = " + log_name)
                # 插入信息
                content = "output =  %s\\n"
                # 插装
                addition = ""
                addition += "%swith open(r\"%s\"%%(sys.version[0:3]), \"w+\", encoding=\'utf8\') as f:\n    %sf.write(\"%s\"%%str(%s))" % (
                    " " * col_offset, log_name, " " * col_offset, content, node.targets[0].id)
                # print(addition)
                source[line_num - 1] += '%s\n' % (addition)
                # print(source[line_num - 1])
                print("插装成功")
            except:
                print("错误：节点属性缺少")

    def visit_Call(self, node):
        pass

        # try:
        #     # xx.xx 不区分方法和构造函数
        #     # re.sub，np.ndarray
        #     print(node.func.value.id, node.func.attr)
        # except:
        #     # 什么时候是attr，什么时候是id
        #     if 'attr' in node.func.__dict__:
        #         print(node.func.attr)
        #     else:
        #         print(node.func.id)
        #     pass


def get_map(json_path):
    with open(json_path, 'r') as f:
        print("解析json，得到系统调用：")
        data = json.load(f)
        # print(data)
        for i in data:
            print(i)
            for sub_class in data[i]['classes']:
                for j in data[i]['classes'][sub_class]:
                    # print(j)
                    flags[j] = 1
            for sub_fun in data[i]['funcs']:
                flags[sub_fun] = 1


def analyse_lib(lib_pathes: list):
    res = {}
    for path in lib_pathes:
        with open(path, encoding='utf8') as f:
            source = f.readlines()
        tmp = ''
        source = tmp.join(source)

        t = ast.parse(source)
        # w().visit(t)

        analyzer = SourceAnalyser()
        analyzer.analyze(t)

        cur_res = {
            'classes': analyzer.all_class,
            'funcs': analyzer.all_func
        }
        # 得到模块的无后缀名字
        module_name = os.path.split(path)[-1].split('.')[0]
        if module_name == '__init__':
            dir_path = os.path.split(path)[0]
            module_name = os.path.split(dir_path)[-1].split('.')[0]
        res[module_name] = cur_res

    with open('module_func_class.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(res, indent=4))

    get_map("module_func_class.json")
    print(flags)


def get_plugin_file(file_path: str, save_path=None, over_write=True):
    r"""

    :param file_path: 待插装的目标文件
    :param save_path: 插装后文件的保存路径，如果为None默认放到与目标文件同一目录下
    :return: 插装之后的文件路径
    """
    print('generating plugin file for % s' % file_path)

    with open(file_path, 'r', encoding='utf8') as f:
        global source, file_parent_path, file_name
        source = f.readlines()
        file_parent_path = os.path.split(file_path)[0]
        file_name = os.path.split(file_path)[-1][0:-3]
        # print(file_parent_path, file_name)

    # log文件夹
    log_path = os.path.join(file_parent_path, 'log')

    if not os.path.exists(log_path):
        os.mkdir(log_path)

    source_str = ''.join(source)
    root = ast.parse(source_str)
    # print(astunparse.dump(root))

    if save_path is None:
        save_path = file_parent_path + "/" + "plugin_" + file_name + ".py"

    if over_write:
        visitor = CallVisitor()
        visitor.visit(root)

        # 插装后代码路径
        source[0] = 'import sys\n' + source[0]
        with open(save_path, "w+", encoding='utf8') as f:
            tmp = ''.join(source)
            f.write(tmp)

    return save_path


if __name__ == "__main__":

    pathes = [r'E:\Anaconda\Lib\re.py',
              r'E:\Anaconda\Lib\os.py',
              r'E:\Anaconda\Lib\site-packages\numpy\__init__.py',
              r'C:\Users\dell\.PyCharm2019.1\system\python_stubs\-727401014\builtins.py',
              ]
    analyse_lib(pathes)

    # 待插装的代码集合
    test_pathes = []
    # 识别目标代码自定义的函数

    for path in test_pathes:
        # path = r'D:\课件\大三上\软件质量测试\大作业\code\Software_test\test.py'
        get_plugin_file(path)
