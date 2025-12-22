from main import part1

def test_part1():
    sample_data = [
        '########',
        '#..O.O.#',
        '##@.O..#',
        '#...O..#',
        '#.#.O..#',
        '#...O..#',
        '#......#',
        '########',
        '',
        '<^^>>>vv<v>>v<<'
    ]
    
    # Preprocess data
    grid = sample_data[:-2]
    moves = sample_data[-1]

    assert part1(grid, moves) == 2028
  