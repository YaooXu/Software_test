import os
import re
import ast
import json
import astunparse
import numpy as np

global source, file_parent_path, file_name
TAB_SIZE = 4
cnt = 0
all_func = {}


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
        if node.name[0] != '_':
            # 忽略私有
            print('func name:', node.name)
            self.all_func.append(node.name)

    def visit_ClassDef(self, node):
        self.all_class[node.name] = []
        print('ClassDef:', node.name)
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.FunctionDef) and sub_node.name[0] != '_':
                # 忽略私有
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


def in_all_func(node, all_func):
    # 判断是不是代码库函数调用
    # 调用方式的不同会使node.value.func中的属性不一样
    if 'attr' in node.value.func.__dict__:
        if node.value.func.attr in all_func:
            print("代码库函数调用：%s" % node.value.func.attr)
            return True
    elif 'id' in node.value.func.__dict__:
        if node.value.func.id in all_func:
            print("代码库函数调用：%s" % node.value.func.id)
            return True

    print("不是代码库函数调用")
    return False


def add_brackets(s):
    # 给字符串加括号
    s = '(' + s + ')'
    return s


def add_quotes(s):
    # 给字符串加双引号
    s = '\"' + s + '\"'
    return s


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
        global cnt

        print("\n------访问Assign节点---")
        line_num = node.lineno

        print("line_num = ", line_num)
        print(source[line_num - 1])
        # print(type(astunparse.dump(node)))
        col_offset = node.col_offset
        if not isinstance(node.value, ast.Call):
            print("节点未调用方法或者函数")
            return

        if not in_all_func(node, all_func):
            # 不是调用的代码库函数
            return

        # 每个log文件的前缀路径
        prefix_log_path = os.path.join(file_parent_path, 'log', file_name + "_" + str(cnt) + "_line" + str(line_num))

        # log中输出内容的前缀信息
        prefix_output = "output = %s\\n"
        prefix_args = "input ="

        if 'id' not in node.value.func.__dict__:
            # *.* 形式的函数调用
            try:
                # 打log
                log_name = prefix_log_path + "_" + node.value.func.value.id + "_" + node.value.func.attr + "_py%s.txt"
                print("log_name = " + log_name)
            except:
                print("错误：节点属性缺少")
                return
        else:
            if node.value.func.id == 'input':
                # 跳过input函数
                return
            # * 形式的函数调用
            try:
                # 打log
                log_name = prefix_log_path + "_" + node.value.func.id + "_py%s.txt"
                print("log_name = " + log_name)
            except:
                print("错误：节点属性缺少")
                return
        try:
            # 第二行参数得多加一个缩进
            addition = "%swith open(r\"%s\"%%(sys.version[0:3]), \"w+\", encoding=\'utf8\') as f:\n%sf.write(\"%s\"%%str(%s))" % (
                " " * col_offset, log_name, " " * (col_offset + TAB_SIZE), prefix_output, node.targets[0].id)
            # print(addition)

            while source[line_num - 1][-2] != ')':
                # 有的函数调用有多行，注意 [-1] 是 \n
                line_num += 1
            source[line_num - 1] += '%s\n' % (addition)
            # print(source[line_num - 1])

            print("插装成功")
            cnt += 1
        except:
            print("错误：节点属性缺少")
            return

        if len(node.value.args):
            # 该函数调用存在参数
            # f.write("input = %s %s %s" % ('x*', '-', str(s)))
            to_print_list = []  # 待打印的参数
            print('参数列表:')
            for arg in node.value.args:
                # 前面的打印形式str加个%s
                prefix_args += " %s"
                # 字符串是s , 变量名是id
                if 's' in arg.__dict__:
                    print(arg.s)
                    to_print_list.append("r\"%s\"" % arg.s)
                elif 'id' in arg.__dict__:
                    print(arg.id)
                    to_print_list.append("str(%s)" % arg.id)
                else:
                    print('参数列表中又无法解析的参数')
                    return

            to_print_str = ",".join(to_print_list)  # 'x*', '-', str(s)
            to_print_str = add_brackets(to_print_str)  # ('x*', '-', str(s))
            prefix_args = add_quotes(prefix_args)  # "input = %s %s %s"

            # 最终插入的语句
            instrument_str = "f.write" + add_brackets(prefix_args + ' % ' + to_print_str)
            # 加上缩进和换行符插入
            source[line_num - 1] += " " * (col_offset + TAB_SIZE) + instrument_str + '\n'
            # print(instrument_str)

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


def load_json(json_path):
    # 加载json中的所有函数
    with open(json_path, 'r') as f:
        print("解析json，得到系统调用：")
        data = json.load(f)
        # print(data)
        for i in data:
            print(i)
            for sub_class in data[i]['classes']:
                for j in data[i]['classes'][sub_class]:
                    # print(j)
                    all_func[j] = 1
            for sub_fun in data[i]['funcs']:
                all_func[sub_fun] = 1


def analyse_lib(lib_pathes: list):
    res = {}
    for path in lib_pathes:
        print('********************************************\n\n%s*' % path)
        with open(path, encoding='utf8') as f:
            source = f.readlines()
        source = ''.join(source)

        t = ast.parse(source)

        analyzer = SourceAnalyser()
        analyzer.analyze(t)

        cur_res = {
            'classes': analyzer.all_class,
            'funcs': analyzer.all_func
        }
        # 得到模块的无后缀名字
        module_name = os.path.split(path)[-1].split('.')[0]
        if module_name == '__init__':
            # 如果有的模块的所有信息在__init__总给出
            # 需要再分割一次路径名
            dir_path = os.path.split(path)[0]
            module_name = os.path.split(dir_path)[-1].split('.')[0]
        res[module_name] = cur_res

    with open('module_func_class.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(res, indent=4))

    load_json("module_func_class.json")
    print(all_func)


def get_instrument_file(file_path: str, save_path=None, over_write=True):
    r"""

    :param file_path: 待插装的目标文件
    :param save_path: 插装后文件的保存路径，如果为None默认放到与目标文件同一目录下
    :return: 插装之后的文件路径
    """
    global cnt
    cnt = 0

    print('generating instrument file for % s' % file_path)

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
        save_path = file_parent_path + "/" + "instrument_" + file_name + ".py"

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
    lib_dir = 'E:\Anaconda\Lib'
    pathes = []
    for root, dir, files in os.walk(lib_dir):
        # 暂时只处理root下的.py文件
        for file in files:
            if file.startswith('_') or file[-2:] != 'py':
                continue
            path = os.path.join(root, file)
            pathes.append(path)
        break
    pathes.append(r'C:\Users\dell\.PyCharm2019.1\system\python_stubs\-727401014\builtins.py')
    analyse_lib(pathes)

    # # 待插装的代码集合
    # test_pathes = []
    # # 识别目标代码自定义的函数
    #
    # for path in test_pathes:
    #     # path = r'D:\课件\大三上\软件质量测试\大作业\code\Software_test\test.py'
    #     get_instrument_file(path)
