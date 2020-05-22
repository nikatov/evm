import numpy as np
from print import print_plate
from helper import distance
from print import print_r_matrix


def sequential_algorithm(matrix, plate_size, info=False):
    plate = [[None] * plate_size[1] for _ in range(plate_size[0])]
    use_list = []
    element = first_element(matrix, use_list, info)
    if info:
        print('Первый элемент:', end=' ')
        print(element)

    use_element(plate, element, (0, 0), use_list)
    if info:
        print('Размещение:')
        print_plate(plate)

    for _ in range(len(matrix) - 1):
        element = next_element(use_list, matrix, use_list, info)
        if info:
            print('следующий элемент:', end=' ')
            print(element)

        candidate_list = candidate_place_list(plate)
        if info:
            print('список кандидатов мест на плате:', end=' ')
            print(candidate_list)

        sum_cost_list = [sum_cost(matrix, plate, element, candidate_place) for candidate_place in candidate_list]
        min_cost_ind = np.array(sum_cost_list).argmin()
        place = candidate_list[min_cost_ind]
        if info:
            print("Значение дельта для выбранных вершин:")
            print(*candidate_list, sep='\t')
            print(*sum_cost_list, sep='\t\t')
            print('Место для размещения элемента:', end=' ')
            print(place)

        use_element(plate, element, place, use_list)
        if info:
            print('Размещение с новым элементом: ')
            print_plate(plate)
            print()
    return plate


def first_element(matrix, use_list, info=False):
    # создание словарей нераспределенных вершин:
    # 1. количество связей с ненулевыми неиспользуемыми вершинами
    # 2. сумма      связей с ненулевыми неиспользуемыми вершинами
    count_dict = dict()
    sum_dict = dict()
    # строки матрицы, соответствующие неиспользуемым вершинам
    for elem, line in [(i, line) for i, line in enumerate(matrix) if i not in use_list]:
        # количество ненулевых связей с вершинами, отсутствующими в списке use_list
        count_dict.update([(elem, len([v for el, v in enumerate(line) if v != 0 and el not in use_list]))])
        # сумма связей с вершинами, отсутствующими в списке use_list
        sum_dict.update([(elem, sum([v for el, v in enumerate(line) if el not in use_list]))])
    if info:
        print('Сумма связей для нераспределенных вершин:')
        print_r_matrix([list(sum_dict.values())], [list(sum_dict.keys())])
    # вершины с минимальной суммой
    elem_list = [i for i, v in sum_dict.items() if v == min(sum_dict.values())]
    # оставляем только вершины с минимальной суммой
    for el in [elem for elem in range(len(matrix)) if elem not in elem_list and elem not in use_list]:
        count_dict.pop(el)
    if info:
        print('Вершины с минимальной суммой внешних связей:', list(count_dict.keys()))
    # вершина с минимальным количеством связей
    value = [el for el in elem_list if count_dict[el] == min(count_dict.values())][0]
    if info and len(count_dict) > 1:
        print('Количество внешних связей для них:')
        print_r_matrix([list(count_dict.values())], [list(count_dict.keys())])
        print('Вершина с минимальным количеством внешних связей:', value)
    return value


def next_element(group, matrix, use_list, info=False):
    adjacent_group = get_adjacent_group(group, matrix, use_list)
    if info:
        print("Перечень неразмещенных вершин, имеющих общие связи с размещенными:", adjacent_group)
    if len(adjacent_group) == 0:
        return first_element(matrix, use_list, info)

    p_list = list(map(sum, matrix))
    delta = dict([(i, 0) for i in adjacent_group])
    for el1 in adjacent_group:
        for el2 in group:
            delta[el1] += matrix[el2][el1] * 2
        delta[el1] -= p_list[el1]
    value, delta = [(i, v) for i, v in delta.items() if v == max(delta.values())][0]
    return value


def get_adjacent_group(group, matrix, use_list):
    adjacent_group = set()
    for el1 in group:
        adjacent_group.update([i for i, el2 in enumerate(matrix[el1]) if el2 != 0 and i not in use_list])
    return list(adjacent_group)


def use_element(plate, element, place, use_list):
    use_list.append(element)
    plate[place[0]][place[1]] = element


def candidate_place_list(plate):
    candidate_set = set()
    for i, p_line in enumerate(plate):
        for j in [ind for ind, place in enumerate(p_line) if place is not None]:
            if 0 < i and plate[i - 1][j] is None:
                candidate_set.add((i - 1, j))
            if i < len(plate) - 1 and plate[i + 1][j] is None:
                candidate_set.add((i + 1, j))
            if 0 < j and plate[i][j - 1] is None:
                candidate_set.add((i, j - 1))
            if j < len(p_line) - 1 and plate[i][j + 1] is None:
                candidate_set.add((i, j + 1))
    return list(candidate_set)


def sum_cost(matrix, plate, element, candidate_place):
    result = 0
    for i, p_line in enumerate(plate):
        for j in [ind for ind, place in enumerate(p_line) if place is not None]:
            result += matrix[element][plate[i][j]] * distance((i, j), candidate_place)
    return result
