'''
--- Day 3: Perfectly Spherical Houses in a Vacuum ---
Santa is delivering presents to an infinite two-dimensional grid of houses.

He begins by delivering a present to the house at his starting location, and then an elf at the North Pole calls him via radio and tells him where to move next. Moves are always exactly one house to the north (^), south (v), east (>), or west (<). After each move, he delivers another present to the house at his new location.

However, the elf back at the north pole has had a little too much eggnog, and so his directions are a little off, and Santa ends up visiting some houses more than once. How many houses receive at least one present?

For example:

> delivers presents to 2 houses: one at the starting location, and one to the east.
^>v< delivers presents to 4 houses in a square, including twice to the house at his starting/ending location.
^v^v^v^v^v delivers a bunch of presents to some very lucky children at only 2 houses.




--- Part Two ---
The next year, to speed up the process, Santa creates a robot version of himself, Robo-Santa, to deliver presents with him.

Santa and Robo-Santa start at the same location (delivering two presents to the same starting house), then take turns moving based on instructions from the elf, who is eggnoggedly reading from the same script as the previous year.

This year, how many houses receive at least one present?

For example:

^v delivers presents to 3 houses, because Santa goes north, and then Robo-Santa goes south.
^>v< now delivers presents to 3 houses, and Santa and Robo-Santa end up back where they started.
^v^v^v^v^v now delivers presents to 11 houses, with Santa going one direction and Robo-Santa going the other.

'''


directions = { '^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1) }

def part1(moves: str) -> int:
    '''
    Given list of move instructions: west (<), east (>), north (^), south (v).
    The Santa starts at (0, 0)
    Return number of distinct houses that the Santa visits following the instructions.

    Parameters:
        moves (str): list of move instructions
        
    Returns:
        int    
    '''
    
    visited = set([(0, 0)])
    x, y = 0, 0
    
    for char in moves:
        dx, dy = directions[char]
        x += dx
        y += dy
        
        visited.add((x, y))
        
    return len(visited)


def part2(instructions: str) -> int:
    '''
    The Santa and the Robo-Sata start from the same location (give 2 presents to that house),
    then taking turn to move and give presents to the other houses following the instructions.
    i.e. The Santa will move following instructions[i], while the Robo-Santa follow instructions[i + 1], and so on.
    Return how many distinct houses that receive the presents.

    Parameters:
        instructions (str): the movement instructions given by the eggnogged elves.
        
    Returns:
        int    
    '''
    
    visited = set([(0, 0)])
    x_santa, y_santa = 0, 0
    x_robo, y_robo = 0, 0
    for i, char in enumerate(instructions):
        dx, dy = directions[char]
        
        if i % 2 == 0:
            x_santa += dx
            y_santa += dy
            visited.add((x_santa, y_santa))
        else:
            x_robo += dx
            y_robo += dy
            visited.add((x_robo, y_robo))
            
    return len(visited)


import os

if __name__ == '__main__':
    data = []
    with open(os.path.join(os.path.dirname(__file__), 'input2.txt'), 'r') as file:
        for line in file.readlines():
            data.append(line.strip())
    
    # print('part 1', part1(data[0]))
    print('part 2', part2(data[0]))
