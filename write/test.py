import re
from socket import socketpair
import numpy as np

if __name__ == '__main__':
    b = []
    b.append('bbb')

    a = re.sub('x*', '-', 'abxd')
    with open("./log_txt/test.txt", "a+", encoding='utf8') as f:
        f.write("line: 9, id = re, attr = sub\n")
    a2 = np.ndarray([1, 2, 3])
    with open("./log_txt/test.txt", "a+", encoding='utf8') as f:
        f.write("line: 10, id = np, attr = ndarray\n")

    c = '1 2 3 4 5'

    d = c.split(' ')
    with open("./log_txt/test.txt", "a+", encoding='utf8') as f:
        f.write("line: 14, id = c, attr = split\n")

    socketpair()

    print("end")
