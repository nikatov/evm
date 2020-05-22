from helper import concat


def print_r_matrix(r_matrix, group_list=None):
    if group_list is None:
        group_list = list([range(len(r_matrix[0]))])
    elem_list = concat(group_list)
    # шапка
    print(end=' R ')
    for el in elem_list:
        if el < 10:
            print(end=' ')
        print(el, end=' ')
    print()

    # столбец + матрица
    for i, line in enumerate(r_matrix):
        # столбец
        if elem_list[i] < 10:
            print(end=' ')
        print(elem_list[i], end='')
        # строка матрицы
        for el in line:
            if el <= -10:
                print(el, end='')
            elif el < 0 or el >= 10:
                print('', el, end='')
            elif el < 10:
                print(' ', el, end='')
        print()


def print_p_matrix(p_matrix, group1, group2):
    # шапка
    print(end='  ')
    for el in group2:
        if el <= -10:
            print('', el, end='')
        elif el < 0 or el >= 10:
            print(' ', el, end='')
        elif el < 10:
            print('  ', el, end='')
    print()

    # столбец + матрица
    for i, line in enumerate(p_matrix):
        # столбец
        if group1[i] < 10:
            print(end=' ')
        print(group1[i], end='')
        # строка матрицы
        for el in line:
            if el <= -10:
                print('', el, end='')
            elif el < 0 or el >= 10:
                print(' ', el, end='')
            elif el < 10:
                print('  ', el, end='')
        print()