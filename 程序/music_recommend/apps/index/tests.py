import re


def check(str):
    my_re = re.compile(r'[A-Za-z]', re.S)
    res = re.findall(my_re, str)
    if len(res):
        return True
    else:
        return False


if __name__ == '__main__':
    str = '你好123hello'

    check(str)

    str1 = '你好123'

    check(str1)
