import sys
import re


def get_line_blocks(fname):
    names = ['C001', 'C002', 'C003', 'C004', 'C005', 'C006', 'C007', 'C008',
             'C009', 'C010', 'C011', 'C012']
    set_dic = {}
    fil = open(fname, 'r')
    lines = fil.readlines()
    start = False
    for line in lines:
        if not start and line.startswith('056:'):
            name = names.pop(0)
            start = True
            the_set = set_dic.setdefault(name, set([]))
        if start:
            lst = line.split('$')[1].strip().split()
            the_set.add(tuple(lst))
        if start and line.startswith('063:'):
            start = False
    return set_dic


if __name__ == '__main__':
    dic = get_line_blocks('./C0012345789012-result.txt')
    x = 1
