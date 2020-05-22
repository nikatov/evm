from print import print_plate
from data import matrix
from sequential_solver import sequential_algorithm
from iterative_solver import iterative_algorithm
from helper import optimal


if __name__ == '__main__':
    plate_size = (5, 6)
    first_plate = sequential_algorithm(matrix, plate_size, info=True)
    second_plate = iterative_algorithm(matrix, first_plate, info=True)

    print_plate(first_plate)
    print('Суммарная длина связей:', optimal(first_plate, matrix))
    print_plate(second_plate)
    print('Суммарная длина связей:', optimal(second_plate, matrix))