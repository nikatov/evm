import numpy as np
import copy
from print import print_p_matrix
from helper import concat


def iterative_algorithm(matrix, all_group_list, info=False):
    group_list = copy.deepcopy(all_group_list)
    for i in range(len(group_list)):
        for j in range(i, len(group_list)):
            group1 = group_list[i]
            group2 = group_list[j]
            alpha1 = [get_a(matrix, el, group1, group2) for el in group1]
            alpha2 = [get_a(matrix, el, group1, group2) for el in group2]
            p_matrix = get_b(matrix, alpha1, alpha2, group1, group2)
            ind1, ind2 = np.unravel_index(p_matrix.argmax(), p_matrix.shape)
            it = 0
            while p_matrix[ind1][ind2] > 0:
                if info:
                    print('Подмножества:', i, 'и', j, ', итерация:', it)
                    print_p_matrix(p_matrix, group1, group2)
                    print('Меняем элементы', group1[ind1], 'и', group2[ind2], 'местами.')
                    print('group_list', group_list)
                    print()
                group1[ind1], group2[ind2] = group2[ind2], group1[ind1]
                alpha1 = [get_a(matrix, el, group1, group2) for el in group1]
                alpha2 = [get_a(matrix, el, group1, group2) for el in group2]
                p_matrix = get_b(matrix, alpha1, alpha2, group1, group2)
                ind1, ind2 = np.unravel_index(p_matrix.argmax(), p_matrix.shape)
                it += 1
            if info:
                print('Подмножества:', i, 'и', j, ', итерация:', it)
                print('Положительных элементов следи всех deltaR больше нет.')
                print()
    return group_list


def iterative_algorithm_v2(matrix, all_group_list, info=False):
    all_group_list = copy.deepcopy(all_group_list)
    for i in range(len(all_group_list) - 1):
        group_list = all_group_list[i:]
        p_matrix = get_b_matrix_v2(matrix, group_list)
        el1, el2 = find_elements_to_swap(p_matrix, group_list)
        iter = 1
        while el1 is not None:
            if info:
                print('Подмножество:', i, ', итерация:', iter)
                print_p_matrix(p_matrix, group_list[0], concat(group_list[1:]))
                print('Меняем элементы', el1, 'и', el2, 'местами.')
                print()
            group_list = swap_group(group_list, el1, el2)
            p_matrix = get_b_matrix_v2(matrix, group_list)
            el1, el2 = find_elements_to_swap(p_matrix, group_list)
            iter += 1
        if info:
            print('Подмножество:', i, ', итерация:', iter)
            print_p_matrix(p_matrix, group_list[0], concat(group_list[1:]))
            print('Положительных элементов следи всех deltaR больше нет.')
            print()
    return all_group_list


def get_a(matrix, v_index, group1, group2):
    alpha = 0
    for el in group1:
        alpha -= matrix[v_index][el]
    for el in group2:
        alpha += matrix[v_index][el]
    if v_index in group2:
        alpha *= -1
    return alpha


def get_b(matrix, alpha1, alpha2, group1, group2):
    b = []
    for i in range(0, len(alpha1)):
        tmp = []
        for j in range(0, len(alpha2)):
            b_value = alpha1[i] + alpha2[j] - 2 * matrix[group1[i]][group2[j]]
            tmp.append(b_value)
        b.append(tmp)
    return np.array(b)


def get_b_v2(elem1, elem2, group_list, matrix):
    val = 0
    for el in group_list[0]:
        val -= matrix[elem1][el]
        val += matrix[elem2][el]
    for group in group_list[1:]:
        if elem2 in group:
            for el in group:
                val += matrix[elem1][el]
                val -= matrix[elem2][el]
    val -= 2 * matrix[elem1][elem2]
    return val


def get_b_matrix_v2(r_matrix, group_list):
    p_matrix = []
    for i, elem in enumerate(group_list[0]):
        p_matrix.append([])
        for j, other_elem in enumerate(concat(group_list[1:])):
            p_matrix[i].append(get_b_v2(elem, other_elem, group_list, r_matrix))
    return np.array(p_matrix)


def find_elements_to_swap(p_matrix, group_list):
    i, j = np.unravel_index(p_matrix.argmax(), p_matrix.shape)
    if p_matrix[i][j] <= 0:
        return None, None
    return group_list[0][i], concat(group_list[1:])[j]


def g_ind(elem, group_list):
    for i, group in enumerate(group_list):
        for j, el in enumerate(group):
            if elem == el:
                return i, j


def swap_group(group_list, elem1, elem2):
    i1, j1 = g_ind(elem1, group_list)
    i2, j2 = g_ind(elem2, group_list)
    group_list[i1][j1], group_list[i2][j2] = group_list[i2][j2], group_list[i1][j1]
    return group_list


def optimal(r_matrix, group_list):
    result = 0
    for i, group1 in enumerate(group_list):
        for group2 in group_list[i + 1:]:
            for el1 in group1:
                for el2 in group2:
                    result += r_matrix[el1][el2]
    return result
