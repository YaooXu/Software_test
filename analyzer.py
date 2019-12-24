import os
import re
import ast
import json
import astunparse


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
        self.all_class[node.name] = []
        print('ClassDef:', node.name)
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.FunctionDef):
                print('func name:', sub_node.name)
                self.all_class[node.name].append(sub_node.name)
        print()

    def visit_Call(self, node):
        # 当前语句的行数
        line_num = node.lineno
        # TODO：打log
        # TODO：判断是否有赋值
        source[line_num - 1] += 'print xxx\n'
        print(source[line_num - 1])
        try:
            # xx.xx 不区分方法和构造函数
            # re.sub，np.ndarray
            print(node.func.value.id, node.func.attr)
        except:
            # TODO：什么时候是attr，什么时候是id
            if 'attr' in node.func.__dict__:
                print(node.func.attr)
            else:
                print(node.func.id)
            pass


if __name__ == "__main__":
    pathes = [r'D:\Anaconda\Anaconda\Lib\re.py',
              r'D:\Anaconda\Anaconda\Lib\os.py']
    res = {}
    for path in pathes:
        with open(path, encoding='utf8') as f:
            source = f.readlines()
        source = ''.join(source)

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
        res[module_name] = cur_res

    with open('test.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(res, indent=4))

    # TODO：识别目标代码自定义的函数
    path = r'D:\课件\大三上\软件质量测试\大作业\code\Software_test\test.py'
    with open(path, encoding='utf8') as f:
        source = f.readlines()
    source2 = ''.join(source)

    root = ast.parse(source2)

    # print(astunparse.dump(root))

    visitor = CallVisitor()
    visitor.visit(root)
