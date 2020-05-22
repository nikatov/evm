from iterative_solver import optimal
from iterative_solver import iterative_algorithm_v2
from sequential_solver import sequential_algorithm
from helper import get_combs
from data import matrix


def main():
    combs = get_combs(min_cont_size=2,
                      max_cont_size=7,
                      element_number=len(matrix))
    group_list_list = []
    new_group_list_list = []
    opt_list = []
    for size_list in combs:
        print(size_list)
        group_list = sequential_algorithm(matrix, size_list)
        group_list_list.append(group_list)

        new_group_list = iterative_algorithm_v2(matrix, group_list)
        new_group_list_list.append(new_group_list)

        opt_list.append(optimal(matrix, new_group_list))

    ind = [i for i, opt in enumerate(opt_list) if opt == min(opt_list)][0]
    print('size_list:', combs[ind])
    print('group_list:', group_list_list[ind])
    print('new_group_list:', new_group_list_list[ind])
    print('opt:', opt_list[ind])


def result():
    size_list = (3, 6, 7, 7, 7)

    old_group_list = sequential_algorithm(matrix, size_list, info=False)
    old_opt = optimal(matrix, old_group_list)

    for i in range(len(old_group_list)):
        old_group_list[i] = sorted(old_group_list[i])

    new_group_list = iterative_algorithm_v2(matrix, old_group_list, info=True)
    new_opt = optimal(matrix, new_group_list)

    print('old_group_list:', old_group_list)
    print('new_group_list:', new_group_list)
    print('old_opt:', old_opt)
    print('new_Q:', new_opt)


if __name__ == '__main__':
    # main()
    result()
