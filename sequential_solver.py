from print import print_r_matrix


def sequential_algorithm(matrix, size_list, info=False):
    group_list = [[] for _ in size_list]
    use_list = []
    for i, (group, size) in enumerate(zip(group_list, size_list)):
        if info:
            print('Группа', i)
        for _ in range(size):
            element = next_element(group, matrix, use_list, info)
            group.append(element)
            if info:
                print('Добавлен вершина', element)
        if info:
            print('В результате руппа', i, ':', group)
            print()
    return group_list


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
    use_list.append(value)
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
    if info:
        print("Значение дельта для выбранных вершин:")
        print_r_matrix([delta.values()], [delta.keys()])
    value, delta = [(i, v) for i, v in delta.items() if v == max(delta.values())][0]
    use_list.append(value)
    return value


def get_adjacent_group(group, matrix, use_list):
    adjacent_group = set()
    for el1 in group:
        adjacent_group.update([i for i, el2 in enumerate(matrix[el1]) if el2 != 0 and i not in use_list])
    return list(adjacent_group)