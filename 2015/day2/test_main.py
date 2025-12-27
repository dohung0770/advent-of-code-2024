from main import part1, part2

def test_part1():
    assert part1([[2, 3, 4]]) == 58
    assert part1([[1, 1, 10]]) == 43


def test_part2():
    assert part2([[2, 3, 4]]) == 34
    assert part2([[1, 1, 10]]) == 14
