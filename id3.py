import time
import math
import sys
from pptree import *


__version__ = '1.0'


def main():
    build_id3()


def get_table(filt):
    global FILENAME
    global readfile_time
    with open(FILENAME) as f:
        columns = f.readline()
        columns = columns[:-1].split(',')
        # table['column']['attribute']['result'] = count
        result_ind = len(columns) - 1
        table = {x: {} for x in columns[:-1]}
        filt_dict = {}

        for key, val in filt.items():
            filt_dict[columns.index(key)] = val
            del table[key]

        i = 0
        for line in f:
            datas = line[:-1].split(',')
            result = datas[result_ind]

            use = True
            for col, val in filt_dict.items():
                if datas[col] != val:
                    use = False
                    break
            if not use:
                continue

            for col_ind in range(result_ind):
                if col_ind in filt_dict:
                    continue
                col = columns[col_ind]
                attr = datas[col_ind]
                if attr not in table[col]:
                    table[col][attr] = {}
                if result not in table[col][attr]:
                    table[col][attr][result] = 0
                table[col][attr][result] += 1
            i += 1
        return table


def build_id3():
    table = get_table({})
    root_name = get_min_entropy(table)
    root = Node(root_name)
    build_tree(root_name, table, {}, root)
    print_tree(root)


def build_tree(root_name, table, filt, node):
    for attr_k, attr in table[root_name].items():
        if len(attr) == 1:
            draw_node(attr_k, attr, node)
        else:
            attr_node = Node('(' + attr_k + ')', node)
            filt[root_name] = attr_k
            new_table = get_table(filt)
            new_col_name = get_min_entropy(new_table)
            new_node = Node(new_col_name, attr_node)
            build_tree(new_col_name, new_table, filt, new_node)
            del filt[root_name]


def draw_node(attr_k, attr, node):
    for i in attr:
        result = i
        break
    attr_k = '(' + attr_k + ')'
    attr_node = Node(attr_k, node)
    Node(result, attr_node)


def get_min_entropy(table):
    min_entropy = 0xffffffff
    min_entropy_k = ''
    for col_k, col in table.items():
        row_len = 0
        attr_len = []
        attr_ent = []
        for attr_k, attr in col.items():
            val = []
            for result_k, result in attr.items():
                val.append(result)

            attr_ent.append(entropy(val))

            val = sum(val)
            row_len += val
            attr_len.append(val)
        gain = 0
        for length, ent in zip(attr_len, attr_ent):
            gain += float(length) / row_len * ent

        if gain < min_entropy:
            min_entropy = gain
            min_entropy_k = col_k

    return min_entropy_k


def entropy(val):
    if len(val) == 1:
        return 0
    total = sum(val)
    result = 0
    for i in val:
        p = float(i) / total
        result -= p * math.log2(p)
    return result

if __name__ == '__main__':
    global FILENAME
    readfile_time = 0
    start_time = time.time()
    FILENAME = sys.argv[1]
    main()
    print('spent: {0}s'.format(time.time() - start_time))
