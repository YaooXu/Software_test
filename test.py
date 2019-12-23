import re

if __name__ == '__main__':
    a = re.sub('x*', '-', 'abxd')

    b = []
    b.append('bbb')

    print(a)
