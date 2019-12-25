import re
from re import sub
from socket import socketpair
import numpy as np
class Test:
    def __init__(self):
        pass

    def split(self):
        a = re.sub('x*', '-', 'abxd')
        with open("./log_txt/test.txt", "a+", encoding='utf8') as f:
            f.write("line: 10, id = re, attr = sub, output =  %s\n"%a)

        return 1

def zzz():
    a = re.sub('x*', '-', 'abxd')
    with open("./log_txt/test.txt", "a+", encoding='utf8') as f:
        f.write("line: 15, id = re, attr = sub, output =  %s\n"%a)
    return a


if __name__ == '__main__':
    a2 = np.ndarray([1, 2, 3])
    b = []
    b.append('bbb')
    a = re.sub('x*', '-', 'abxd')
    with open("./log_txt/test.txt", "a+", encoding='utf8') as f:
        f.write("line: 23, id = re, attr = sub, output =  %s\n"%a)
    a = sub('x*', '-', 'abxd')
    with open("./log_txt/test.txt", "a+", encoding='utf8') as f:
        f.write("line: 24, attr = sub, output =  %s\n"%a)
    x = zzz()
    with open("./log_txt/test.txt", "a+", encoding='utf8') as f:
        f.write("line: 25, attr = zzz, output =  %s\n"%x)
    c = '1 2 3 4 5'
    d = c.split(' ')
    with open("./log_txt/test.txt", "a+", encoding='utf8') as f:
        f.write("line: 27, id = c, attr = split, output =  %s\n"%d)
    socketpair()

    print("end")
