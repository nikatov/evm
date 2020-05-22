from itertools import combinations_with_replacement


def concat(ll):
    return [el for lst in ll for el in lst]


def get_combs(min_cont_size,
              max_cont_size,
              element_number):
    min_comb_size = (element_number - 1) // max_cont_size + 1
    max_comb_size = (element_number - 1) // min_cont_size + 1
    combs = []
    for comb_size in range(min_comb_size, max_comb_size + 1):
        combs += list(combinations_with_replacement(range(min_cont_size, max_cont_size + 1), comb_size))
    return [cont for cont in combs if sum(cont) == element_number]