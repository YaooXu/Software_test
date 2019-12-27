import sys

if __name__ == "__main__":

    filename = "test.txt"
    path = "./write/" + filename
    with open(path, "a+",encoding='utf8') as f:
        # TODO:插入信息
        content = "insert"
        f.write(content)
    print(sys.version[0:5])
