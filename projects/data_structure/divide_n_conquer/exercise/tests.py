
test0 = {
    'input': {
        'poly1': [2, 0, 5, 7],
        'poly2': [3, 4, 2]
    },
    'output': [6, 8, 19, 41, 38, 14]
}
test1 = {
    'input': {
        'poly1': [3, 7, 9, 10, 15, 30],
        'poly2': [4, 6, 9, 11, 14]
    },
    'output': [12, 46, 105, 190, 320, 497, 551, 575, 540, 420]
}
test2 = {
    'input': {
        'poly1': [1, 2, 3, 4],
        'poly2': [0, 2, 5]
    },
    'output': [0, 2, 9, 16, 23, 20]
}
test3 = {
    'input': {
        'poly1': [0, 7, 3, 6],
        'poly2': [3, 4, 8]
    },
    'output': [0, 21, 37, 86, 48, 48]
}
test4 = {
    'input': {
        'poly1': [2, 2, 4, 4],
        'poly2': [3, 5, 7]
    },
    'output': [6, 16, 36, 46, 48, 28]
}
test5 = {
    'input': {
        'poly1': [4, 6, 8],
        'poly2': [9, 3]
    },
    'output': [36, 66, 90, 24]
}
test6 = {
    'input': {
        'poly1': [5, 7, 9, 12, 17],
        'poly2': [11, 3, 7, 9]
    },
    'output': [55, 92, 155, 253, 349, 216, 227, 153]
}
tests = [test0, test1, test2, test3, test4, test5, test6]


# List of numbers in random order
random_test0 = {
    'input': {
        'nums': [4, 2, 6, 3, 4, 6, 2, 1]
    },
    'output': [1, 2, 2, 3, 4, 4, 6, 6]
}
# List of numbers in random order
random_test1 = {
    'input': {
        'nums': [5, 2, 6, 1, 23, 7, -12, 12, -243, 0]
    },
    'output': [-243, -12, 0, 1, 2, 5, 6, 7, 12, 23]
}
# A list that's already sorted
random_test2 = {
    'input': {
        'nums': [3, 5, 6, 8, 9, 10, 99]
    },
    'output': [3, 5, 6, 8, 9, 10, 99]
}
# A list that's sorted in descending order
random_test3 = {
    'input': {
        'nums': [99, 10, 9, 8, 6, 5, 3]
    },
    'output': [3, 5, 6, 8, 9, 10, 99]
}
# A list containing repeating elements
random_test4 = {
    'input': {
        'nums': [5, -12, 2, 6, 1, 23, 7, 7, -12, 6, 12, 1, -243, 1, 0]
    },
    'output': [-243, -12, -12, 0, 1, 1, 1, 2, 5, 6, 6, 7, 7, 12, 23]
}
# An empty list
random_test5 = {
    'input': {
        'nums': []
    },
    'output': []
}
# A list containing just one element
random_test6 = {
    'input': {
        'nums': [23]
    },
    'output': [23]
}
# A list containing one element repeated many times
random_test7 = {
    'input': {
        'nums': [42, 42, 42, 42, 42, 42, 42]
    },
    'output': [42, 42, 42, 42, 42, 42, 42]
}

import random
in_list = list(range(10000))
out_list = list(range(10000))
random.shuffle(in_list)
random_test8 = {
    'input': {
        'nums': in_list
    },
    'output': out_list
}
random_tests = [random_test0, random_test1, random_test2, random_test3, random_test4,
                random_test5, random_test6, random_test7, random_test8]
