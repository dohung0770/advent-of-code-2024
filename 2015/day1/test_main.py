from main import part1, part2

def test_part1():
    assert part1('(())') == 0
    assert part1('()()') == 0
    assert part1('(((') == 3
    assert part1('(()(()(') == 3
    assert part1('))(((((') == 3
    assert part1('())') == -1
    assert part1('))(') == -1
    assert part1(')))') == -3
    assert part1(')())())') == -3
    
def test_part2():
    assert part2(')') == 1
