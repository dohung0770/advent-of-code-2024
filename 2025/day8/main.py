'''
--- Day 8: Playground ---
Equipped with a new understanding of teleporter maintenance, you confidently step onto the repaired teleporter pad.

You rematerialize on an unfamiliar teleporter pad and find yourself in a vast underground space which contains a giant playground!

Across the playground, a group of Elves are working on setting up an ambitious Christmas decoration project. Through careful rigging, they have suspended a large number of small electrical junction boxes.

Their plan is to connect the junction boxes with long strings of lights. Most of the junction boxes don't provide electricity; however, when two junction boxes are connected by a string of lights, electricity can pass between those two junction boxes.

The Elves are trying to figure out which junction boxes to connect so that electricity can reach every junction box. They even have a list of all of the junction boxes' positions in 3D space (your puzzle input).

For example:

162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
This list describes the position of 20 junction boxes, one per line. Each position is given as X,Y,Z coordinates. So, the first junction box in the list is at X=162, Y=817, Z=812.

To save on string lights, the Elves would like to focus on connecting pairs of junction boxes that are as close together as possible according to straight-line distance. In this example, the two junction boxes which are closest together are 162,817,812 and 425,690,689.

By connecting these two junction boxes together, because electricity can flow between them, they become part of the same circuit. After connecting them, there is a single circuit which contains two junction boxes, and the remaining 18 junction boxes remain in their own individual circuits.

Now, the two junction boxes which are closest together but aren't already directly connected are 162,817,812 and 431,825,988. After connecting them, since 162,817,812 is already connected to another junction box, there is now a single circuit which contains three junction boxes and an additional 17 circuits which contain one junction box each.

The next two junction boxes to connect are 906,360,560 and 805,96,715. After connecting them, there is a circuit containing 3 junction boxes, a circuit containing 2 junction boxes, and 15 circuits which contain one junction box each.

The next two junction boxes are 431,825,988 and 425,690,689. Because these two junction boxes were already in the same circuit, nothing happens!

This process continues for a while, and the Elves are concerned that they don't have enough extension cables for all these circuits. They would like to know how big the circuits will be.

After making the ten shortest connections, there are 11 circuits: one circuit which contains 5 junction boxes, one circuit which contains 4 junction boxes, two circuits which contain 2 junction boxes each, and seven circuits which each contain a single junction box. Multiplying together the sizes of the three largest circuits (5, 4, and one of the circuits of size 2) produces 40.

Your list contains many junction boxes; connect together the 1000 pairs of junction boxes which are closest together. Afterward, what do you get if you multiply together the sizes of the three largest circuits?
'''

sample_data = [
  '162,817,812',
  '57,618,57',
  '906,360,560',
  '592,479,940',
  '352,342,300',
  '466,668,158',
  '542,29,236',
  '431,825,988',
  '739,650,466',
  '52,470,668',
  '216,146,977',
  '819,987,18',
  '117,168,530',
  '805,96,715',
  '346,949,466',
  '970,615,88',
  '941,993,340',
  '862,61,35',
  '984,92,344',
  '425,690,689'
]

import math
import heapq

def ecludean_distance(pos1: list[int], pos2: list[int]) -> int:
  return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2 + (pos1[2] - pos2[2]) ** 2)



def part1(grid: list[list[int]], max_pairs: int) -> int:
  '''
  Return the product of sizes of 3 largest circuits after connecting 1000 pairs of shortest junction boxes
  The distance between any two boxes are determined by the ecludean distance. i.e. in 3D: sqrt((x1 - x2)^2 + (y1 - y2)^2 + (z1 - x2)^2)
  
  :param grid: grid of junction boxes in 3D (x, y, z)
  :type grid: list[list[int]]
  :param max_pairs: maximum number of pairs of junctions boxes with shortest distance will be connected
  :type max_pairs: int
  :return: the product of sizes of the 3 largest circuits after connecting at most 'max_pairs' pairs of closest junction boxes
  :rtype: int
  '''

  n = len(grid)
  heap = [] # max heap

  for i in range(n - 1):
    for j in range(i + 1, n):
      dist = -ecludean_distance(grid[i], grid[j])

      if len(heap) < max_pairs:
        heapq.heappush(heap, (dist, i, j))
      elif heap[0][0] < dist:
        heapq.heappushpop(heap, (dist, i, j))

  # union-find
  parent = [node for node in range(n)]
  size = [1] * n

  def find(node: int) -> int:
    if parent[node] != node:
      parent[node] = find(parent[node])

    return parent[node]
  
  def unify(node1: int, node2: int):
    p1, p2 = find(node1), find(node2)

    if p1 == p2:
      return
    
    if size[p1] >= size[p2]:
      parent[p2] = p1
      size[p1] += size[p2]
    else:
      parent[p1] = p2
      size[p2] += size[p1]

  while heap:
    _, i, j = heapq.heappop(heap)

    unify(i, j)

  largest, second, third = 1, 1, 1
  for node in range(n):
    if find(node) == node:
      sz = size[node]
      
      if largest < sz:
        third = second
        second = largest
        largest = sz
      elif second < sz:
        third = second
        second = sz
      elif third < sz:
        third = sz

  return largest * second * third

import os

data = []
with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as file:
  for line in file.readlines():
    data.append(line.strip())

# print(part1([list(map(int, line.split(','))) for line in sample_data], max_pairs=10))
# print(part1([list(map(int, line.split(','))) for line in data], max_pairs=1000))


'''
--- Part Two ---
The Elves were right; they definitely don't have enough extension cables. You'll need to keep connecting junction boxes together until they're all in one large circuit.

Continuing the above example, the first connection which causes all of the junction boxes to form a single circuit is between the junction boxes at 216,146,977 and 117,168,530. The Elves need to know how far those junction boxes are from the wall so they can pick the right extension cable; multiplying the X coordinates of those two junction boxes (216 and 117) produces 25272.

Continue connecting the closest unconnected pairs of junction boxes together until they're all in the same circuit. What do you get if you multiply together the X coordinates of the last two junction boxes you need to connect?
'''

def part2(grid: list[list[int]]) -> int:
  '''
  Return the product of x coordinates of the last two junction boxes you need to connect in order to form one giant circuit
  
  :param grid: grid of junction boxes in 3D (x, y, z)
  :type grid: list[list[int]]
  :return: product of x coordinates of the last two boxes to connect
  :rtype: int
  '''

  n = len(grid)
  heap = [] # min heap

  for i in range(n - 1):
    for j in range(i + 1, n):
      dist = ecludean_distance(grid[i], grid[j])
      heapq.heappush(heap, (dist, i, j))

  # union-find
  parent = [node for node in range(n)]
  size = [1] * n

  def find(node: int) -> int:
    if parent[node] != node:
      parent[node] = find(parent[node])

    return parent[node]
  
  rem_boxes = n # number of standalone junction boxes
  
  def unify(node1: int, node2: int) -> int:
    p1, p2 = find(node1), find(node2)

    if p1 == p2:
      return 0
    
    if size[p1] >= size[p2]:
      parent[p2] = p1
      size[p1] += size[p2]
    else:
      parent[p1] = p2
      size[p2] += size[p1]

    return 1

  while heap:
    _, i, j = heapq.heappop(heap)
    rem_boxes -= unify(i, j)

    if rem_boxes == 1:
      return grid[i][0] * grid[j][0]
    
  return 0

# print(part2([list(map(int, line.split(','))) for line in sample_data]))
print(part2([list(map(int, line.split(','))) for line in data]))

