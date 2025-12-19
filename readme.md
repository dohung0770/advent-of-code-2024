input.txt -> dohung0770@gmail.com
input2.txt -> hungdow07@gmail.com


# Template
```python

'''
'''

import os


def part1() -> int:
    '''
    Summary

    Parameters:
        a (int): description

    Returns:
        int
    '''
    pass


def part2() -> int:
    '''
    Summary

    Parameters:
        a (int): description

    Returns:
        int
    '''
    pass


if __name__ == '__main__':
    sample_data = []

    data = []

    with open(os.path.join(os.path.dirname(__file__), 'input2.txt'), 'r') as file:
        for line in file.readlines():
            data.append(line.strip())

    # Preprocess data

    print('---- Part 1 ----')
    print('result = ', part1())

    print('---- Part 2 ----')
    print('result = ', part2())
```
