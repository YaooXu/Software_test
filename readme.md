# 项目说明
该大作业任务为找到某种语言不同版本之间不同的API输出，本项目比较的是python3.3和python3.8的区别，具体内容见下

## 1、文件树结构

#### source	

包括测试用的源代码文件、产生的所有结果文件、比较后有差异的文件

- codeforce_1000  **从codeforce网站爬取的代码**
  - 1000.py   **测试源代码**
  - input.txt  **测试输入**
  - instrument_1000.py **插装之后的代码**
  - log
    - 1000_1_linexx_re_sub_py3.6.txt **在存在系统调用的地方打印输出**

- codeforce_702
  - 702.py
  - input.txt
  - instrument_702.py
  - log
    - 702_1_linexx_c_split_py3.6.txt 
- ……

- docs           **从python官方文档爬取的测试代码**
- w3c            **从w3c网站上爬取的代码**
- compare_result.txt      **比较后有差异的文件**



#### analyzer.py

用于分析源代码，进行插装的程序



#### compare.py

用于比较插装代码打印的输出



#### get_codeforce_request.py

从codeforce网站爬取ACM测试代码



#### get_codeforces_selenium.py

从codeforce网站爬取ACM测试代码



#### get_testcase_docs.py

从python官方文档中爬取测试代码



#### get_testcase_w3c.py

从w3c网站上爬取测试代码



#### module_func_class.json

从系统库中分析找出的系统调用API



#### run_all.py

主程序运行入口



## 2、Difference

- [1 re.sub()](#_Toc30192716)
- [2 re.split()](#_Toc30192717)
- [3 startswith()](#_Toc30192718)
- [4 endswith()](#_Toc30192719)
- [5 bytes.fromhex()](#_Toc30192720)
- [6 os.dup2()](#_Toc30192721)
- [7 parser.sections()](#_Toc30192722)
- [8 pickle.dumps()](#_Toc30192723)
- [9 fnmatch.translate()](#_Toc30192724)
- [10 json.dumps()](#_Toc30192725)
- [11 os.stat()](#_Toc30192726)
- [12 signature()](#_Toc30192727)









