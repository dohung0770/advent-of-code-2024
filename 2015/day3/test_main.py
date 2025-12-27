from main import part1, part2


def test_part1():
    assert part1('>') == 2
    assert part1('^>v<') == 4
    assert part1('^v^v^v^v^v') == 2
    
def test_part2():
    assert part2('^v') == 3
    assert part2('^>v<') == 3
    assert part2('^v^v^v^v^v') == 11
