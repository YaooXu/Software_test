## TODO
- ~~规范插装的语句~~
- ~~爬虫规范一下文件夹和文件命令~~
- ~~爬虫的input存在问题~~
    - ~~存在空行~~
    - ~~有的没有分行~~
- ~~爬虫加上已存在题号判断~~
- 优化比较文件的输出形式，过滤掉一点没用的比较
- log文件名中会出现c_split，而我们更希望是str_split
    - 插装中判断是不是变量，如果是变量则引入type(c),而不是c
- 区分类的方法调用和函数调用
- 爬取更多的代码库的方法和函数

### 文件树结构

source

- codeforce_1000
  - 1000.py
  - input.txt
  - instrument_1000.py
  - log
    - 1000_1_linexx_re_sub_py3.6.txt
- codeforce_702
  - 702.py
  - input.txt
  - instrument_702.py
  - log
    - 702_1_linexx_c_split_py3.6.txt 

### 还需要跑的代码



### Difference

#### 可以直接使用

- Before Python 3.5, a [`datetime.time`](https://docs.python.org/3.5/library/datetime.html#datetime.time) object was considered to be false if it represented midnight in UTC. This behavior was considered obscure and error-prone and has been removed in Python 3.5.
- The [`re.split()`](https://docs.python.org/3.5/library/re.html#re.split) function always ignored empty pattern matches, so the `"x*"` pattern worked the same as `"x+"`, and the `"\b"` pattern never worked. Now [`re.split()`](https://docs.python.org/3.5/library/re.html#re.split) raises a warning if the pattern could match an empty string. For compatibility, use patterns that never match an empty string (e.g. `"x+"` instead of `"x*"`). Patterns that could only match an empty string (such as `"\b"`) now raise an error.
- The [`str.startswith()`](https://docs.python.org/3.5/library/stdtypes.html#str.startswith) and [`str.endswith()`](https://docs.python.org/3.5/library/stdtypes.html#str.endswith) methods no longer return `True` when finding the empty string and the indexes are completely out of range. 
- [`re.sub()`](https://docs.python.org/3/library/re.html#re.sub) now replaces empty matches adjacent to a previous non-empty match. For example `re.sub('x*', '-', 'abxd')` returns now `'-a-b--d-'` instead of `'-a-b-d-'` (the first minus between ‘b’ and ‘d’ replaces ‘x’, and the second minus replaces an empty string between ‘x’ and ‘d’).
- os.dup2
- bytes.fromhex



