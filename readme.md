## TODO
- ~~规范插装的语句~~
- ~~爬虫规范一下文件夹和文件命令~~
- log文件名中会出现c_split，而我们更希望是str_split
- 区分类的方法调用和函数调用
- 爬虫加上已存在题号判断
- 爬虫的input存在问题
    - 存在空行
    - 有的没有分行

### 文件树结构

source

- codeforce_1000
  - 1000.py
  - input.txt
  - plugin_1000.py
  - log
    - 1000_1_linexx_re_sub_py3.6.txt
- codeforce_702
  - 702.py
  - input.txt
  - plugin_702.py
  - log
    - 702_1_linexx_c_split_py3.6.txt 

### Difference

#### 可以直接使用

- [`re.sub()`](https://docs.python.org/3/library/re.html#re.sub) now replaces empty matches adjacent to a previous non-empty match. For example `re.sub('x*', '-', 'abxd')` returns now `'-a-b--d-'` instead of `'-a-b-d-'` (the first minus between ‘b’ and ‘d’ replaces ‘x’, and the second minus replaces an empty string between ‘x’ and ‘d’).