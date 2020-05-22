from helper import distance
from helper import optimal
from print import print_plate
import numpy as np
import copy

def iterative_algorithm(matrix, plate, info=False):
    plate = copy.deepcopy(plate)
    if info:
        print_plate(plate)
    while True:
        #  Вычисляем среднюю длину связей каждой вершины
        avg_len_list = [sum_len(matrix, plate, (i, j)) for i in range(len(plate)) for j in range(len(plate[0]))]
        #  Находим вершину с наибольшим значением средней длины связи
        point = [(i, j) for i in range(len(plate)) for j in range(len(plate[0])) if sum_len(matrix, plate, (i, j)) == max(avg_len_list)][0]
        if info:
            print('Средняя длина связей каждой вершины:')
            for i in range(len(plate)):
                for j in range(len(plate[i])):
                    print(sum_len(matrix, plate, (i, j)), end='\t')
                print()
        #  Находим ее центр массы
        mass_center_p = mass_center(matrix, plate, point)
        #  Находим вершины-кандидаты для перестановки
        candidate_list = candidate_place_list(plate, *mass_center_p)
        #  Совершаем пробные перестановки с вершинами-кандидатами
        delta_list = get_delta_list(matrix, plate, point, candidate_list)
        if info:
            print('Наихудшим образом расположенная вершина:', plate[point[0]][point[1]])
            print('Ее центр масс связей в точке:', mass_center_p)
            print('Вершины вблизи ее центра масс, их координаты и величина,'
                  'на которую изменится сумма связей при перестановке:')
            for p, v in zip(candidate_list, delta_list):
                print(plate[p[0]][p[1]], p, v)
        if min(delta_list) >= 0:
            if info:
                print('Перестановок больше нет')
            return plate
        point_to_swap = candidate_list[np.array(delta_list).argmin()]
        if info:
            print('Вершина для перестановки:', point_to_swap)
            print(plate[point[0]][point[1]], ' меняются с', plate[point_to_swap[0]][point_to_swap[1]])
        swap_element(plate, *point, *point_to_swap)
        if info:
            print('Q = ', optimal(plate, matrix))
            print('Новое размещение: ')
            print_plate(plate)


def candidate_place_list(plate, ind_i, ind_j):
    place_list = set()
    ind_i = int(ind_i + (0.5 if ind_i > 0 else -0.5))  # округление
    ind_j = int(ind_j + (0.5 if ind_j > 0 else -0.5))  # округление
    for i in range(ind_i - 1, ind_i + 2):
        for j in range(ind_j - 1, ind_j + 2):
            # координаты за пределами платы не рассматриваются
            if i < 0 or j < 0 or i >= len(plate) or j >= len(plate[0]):
                continue
            place_list.add((i, j))
    return list(place_list)


def sum_len(matrix, plate, point):
    element = plate[point[0]][point[1]]
    result = 0
    for i, p_line in enumerate(plate):
        for j in [ind for ind, place in enumerate(p_line)]:
            result += matrix[element][plate[i][j]] * distance((i, j), point)
    return result


def average_len(matrix, plate, point):
    element = plate[point[0]][point[1]]
    return sum_len(matrix, plate, point) / sum(matrix[element])


def mass_center(matrix, plate, point):
    element = plate[point[0]][point[1]]
    mass_i = 0
    mass_j = 0
    for i, p_line in enumerate(plate):
        for j in [ind for ind, place in enumerate(p_line) if place is not None]:
            mass_i += matrix[element][plate[i][j]] * np.abs(i - point[0])
            mass_j += matrix[element][plate[i][j]] * np.abs(j - point[1])
    return mass_i / sum(matrix[element]), mass_j / sum(matrix[element])


def swap_element(plate, i1, j1, i2, j2):
    plate[i1][j1], plate[i2][j2] = plate[i2][j2], plate[i1][j1]


def get_delta_list(matrix, plate, point, candidate_list):
    delta_list = []
    for candidate in candidate_list:
        s1 = sum_len(matrix, plate, candidate) + sum_len(matrix, plate, point)
        swap_element(plate, *candidate, *point)
        s2 = sum_len(matrix, plate, candidate) + sum_len(matrix, plate, point)
        swap_element(plate, *candidate, *point)
        delta_list.append(s2 - s1)
    return delta_list
