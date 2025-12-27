'''
--- Day 9: Movie Theater ---
You slide down the firepole in the corner of the playground and land in the North Pole base movie theater!

The movie theater has a big tile floor with an interesting pattern. Elves here are redecorating the theater by switching out some of the square tiles in the big grid they form. Some of the tiles are red; the Elves would like to find the largest rectangle that uses red tiles for two of its opposite corners. They even have a list of where the red tiles are located in the grid (your puzzle input).

For example:

7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
Showing red tiles as # and other tiles as ., the above arrangement of red tiles would look like this:

..............
.......#...#..
..............
..#....#......
..............
..#......#....
..............
.........#.#..
..............
You can choose any two red tiles as the opposite corners of your rectangle; your goal is to find the largest rectangle possible.

For example, you could make a rectangle (shown as O) with an area of 24 between 2,5 and 9,7:

..............
.......#...#..
..............
..#....#......
..............
..OOOOOOOO....
..OOOOOOOO....
..OOOOOOOO.#..
..............
Or, you could make a rectangle with area 35 between 7,1 and 11,7:

..............
.......OOOOO..
.......OOOOO..
..#....OOOOO..
.......OOOOO..
..#....OOOOO..
.......OOOOO..
.......OOOOO..
..............
You could even make a thin rectangle with an area of only 6 between 7,3 and 2,3:

..............
.......#...#..
..............
..OOOOOO......
..............
..#......#....
..............
.........#.#..
..............
Ultimately, the largest rectangle you can make in this example has area 50. One way to do this is between 2,5 and 11,1:

..............
..OOOOOOOOOO..
..OOOOOOOOOO..
..OOOOOOOOOO..
..OOOOOOOOOO..
..OOOOOOOOOO..
..............
.........#.#..
..............
Using two red tiles as opposite corners, what is the largest area of any rectangle you can make?


'''

sample_data = [
  '7,1',
  '11,1',
  '11,7',
  '9,7',
  '9,5',
  '2,5',
  '2,3',
  '7,3'
]

def part1(pos: list[list[int]]) -> int:
  '''
  Returns the maximum rectangle area formed by selecting 2 red tiles in 'pos' are 2 opposite corners of that rectangle
  
  :param pos: positions of red tiles
  :type pos: list[list[int]]
  :return: maximum area of any rectangle formed by 2 red tiles as the opposite corners
  :rtype: int
  '''

  # Brute force?
  n = len(pos)
  max_area = 0
  for i in range(n - 1):
    for j in range(i + 1, n):
      max_area = max(max_area, (abs(pos[j][0] - pos[i][0]) + 1) * (abs(pos[j][1] - pos[i][1]) + 1))

  return max_area

import os

data = []
with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as file:
  for line in file.readlines():
    data.append(line.strip())

# print(part1(
#   [list(map(int, line.split(','))) for line in sample_data]
# ))
# print(part1(
#   [list(map(int, line.split(','))) for line in data]
# ))


'''
--- Part Two ---
The Elves just remembered: they can only switch out tiles that are red or green. So, your rectangle can only include red or green tiles.

In your list, every red tile is connected to the red tile before and after it by a straight line of green tiles. The list wraps, so the first red tile is also connected to the last red tile. Tiles that are adjacent in your list will always be on either the same row or the same column.

Using the same example as before, the tiles marked X would be green:

..............
.......#XXX#..
.......X...X..
..#XXXX#...X..
..X........X..
..#XXXXXX#.X..
.........X.X..
.........#X#..
..............
In addition, all of the tiles inside this loop of red and green tiles are also green. So, in this example, these are the green tiles:

..............
.......#XXX#..
.......XXXXX..
..#XXXX#XXXX..
..XXXXXXXXXX..
..#XXXXXX#XX..
.........XXX..
.........#X#..
..............
The remaining tiles are never red nor green.

The rectangle you choose still must have red tiles in opposite corners, but any other tiles it includes must now be red or green. This significantly limits your options.

For example, you could make a rectangle out of red and green tiles with an area of 15 between 7,3 and 11,1:

..............
.......OOOOO..
.......OOOOO..
..#XXXXOOOOO..
..XXXXXXXXXX..
..#XXXXXX#XX..
.........XXX..
.........#X#..
..............
Or, you could make a thin rectangle with an area of 3 between 9,7 and 9,5:

..............
.......#XXX#..
.......XXXXX..
..#XXXX#XXXX..
..XXXXXXXXXX..
..#XXXXXXOXX..
.........OXX..
.........OX#..
..............
The largest rectangle you can make in this example using only red and green tiles has area 24. One way to do this is between 9,5 and 2,3:

..............
.......#XXX#..
.......XXXXX..
..OOOOOOOOXX..
..OOOOOOOOXX..
..OOOOOOOOXX..
.........XXX..
.........#X#..
..............
Using two red tiles as opposite corners, what is the largest area of any rectangle you can make using only red and green tiles?


'''

from typing import Callable

def part2(pos: list[list[int]]) -> int:
  '''
  All the red tiles are connected in the same row or column by green tiles, and the list is wrapped,
    so there will always be a connected region that is filled with either red or green

  Returns the maximum rectangle area that contains only green (X) or red (#) inside it
  
  :param pos: list of red tiles positions
  :type pos: list[list[int]]
  :return: the maximum rectangle area
  :rtype: int
  '''

  # Prefix sum + Binary search
  n = len(pos)
  # y_coords = set()
  # for _, y in pos:
  #   y_coords.add(y - 1)
  #   y_coords.add(y)
  #   y_coords.add(y)

  # y_map = dict()

  # val = 0
  # for y in y_coords:
  #   if y not in y_map:
  #     y_map[y] = val
  #     val += 1

  # N = val

  # y_pref = [1] * N
  # y_suff = [1] * N

  max_area = 0
  for i in range(n - 1):
    x1, y1 = pos[i]
    for j in range(i + 1, n):
      x2, y2 = pos[j]

      if find(pos, lambda x, y: x <= min(x1, x2) and y >= max(y1, y2)) and \
        find(pos, lambda x, y: x <= min(x1, x2) and y <= min(y1, y2)) and \
        find(pos, lambda x, y: x >= max(x1, x2) and y <= min(y1, y2)) and \
        find(pos, lambda x, y: x >= max(x1, x2) and y >= max(y1, y2)):
        max_area = max(max_area, (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1))

  return max_area

def find(pos: list[list[int]], check: Callable[[int, int], bool]) -> bool:
  for x, y in pos:
    if check(x, y):
      return True
    
  return False

# print(part2(
#   [list(map(int, line.split(','))) for line in sample_data]
# ))
print(part2(
  [list(map(int, line.split(','))) for line in data]
))