import numpy as np


def concat(ll):
    return [el for lst in ll for el in lst]


def distance(point1, point2):
    return np.abs(point1[0] - point2[0]) + np.abs(point1[1] - point2[1])


def optimal(plate, matrix):
    result = 0
    for i, line1 in enumerate(plate):
        for j, el1 in enumerate(line1):
            for i2, line2 in enumerate(plate):
                for j2, el2 in enumerate(line2):
                    if el1 < el2:
                        result += matrix[el1][el2] * distance((i, j), (i2, j2))
    return result