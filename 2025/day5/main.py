'''
--- Day 5: Cafeteria ---
As the forklifts break through the wall, the Elves are delighted to discover that there was a cafeteria on the other side after all.

You can hear a commotion coming from the kitchen. "At this rate, we won't have any time left to put the wreaths up in the dining hall!" Resolute in your quest, you investigate.

"If only we hadn't switched to the new inventory management system right before Christmas!" another Elf exclaims. You ask what's going on.

The Elves in the kitchen explain the situation: because of their complicated new inventory management system, they can't figure out which of their ingredients are fresh and which are spoiled. When you ask how it works, they give you a copy of their database (your puzzle input).

The database operates on ingredient IDs. It consists of a list of fresh ingredient ID ranges, a blank line, and a list of available ingredient IDs. For example:

3-5
10-14
16-20
12-18

1
5
8
11
17
32
The fresh ID ranges are inclusive: the range 3-5 means that ingredient IDs 3, 4, and 5 are all fresh. The ranges can also overlap; an ingredient ID is fresh if it is in any range.

The Elves are trying to determine which of the available ingredient IDs are fresh. In this example, this is done as follows:

Ingredient ID 1 is spoiled because it does not fall into any range.
Ingredient ID 5 is fresh because it falls into range 3-5.
Ingredient ID 8 is spoiled.
Ingredient ID 11 is fresh because it falls into range 10-14.
Ingredient ID 17 is fresh because it falls into range 16-20 as well as range 12-18.
Ingredient ID 32 is spoiled.
So, in this example, 3 of the available ingredient IDs are fresh.

Process the database file from the new inventory management system. How many of the available ingredient IDs are fresh?
'''

sample_data = [
  [[3, 5], [10, 14], [16, 20], [12, 18]],
  [1, 5, 8, 11, 17, 32]
]

def part1(fresh_id_ranges: list[list[int]], ingredient_ids: list[int]) -> int:
  # Linesweeping + Coordinate compression

  nums = set(ingredient_ids)
  for start, end in fresh_id_ranges:
    nums.add(start)
    nums.add(end)
    nums.add(end + 1)

  coord_map = dict()
  value = 1
  for num in sorted(list(nums)):
    coord_map[num] = value
    value += 1

  min_id = min([coord_map[start] for start, _ in fresh_id_ranges])
  max_id = max([coord_map[end] for _, end in fresh_id_ranges])
  N = max_id - min_id + 1
  pref = [0] * (N + 1)

  for start, end in fresh_id_ranges:
    pref[coord_map[start] - min_id] += 1
    pref[coord_map[end] - min_id + 1] -= 1

  for i in range(1, len(pref)):
    pref[i] += pref[i - 1]

  fresh_cnt = 0
  for id in ingredient_ids:
    id = coord_map[id]
    if min_id <= id <= max_id and pref[id - min_id] > 0:
      fresh_cnt += 1

  return fresh_cnt


import os

fresh_id_ranges = []
ingredient_ids = []
flag = 0
with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as file:
  lines = file.readlines()

  for line in lines:
    if not line.strip():
      flag = 1
      continue

    if flag == 1:
      ingredient_ids.append(int(line.strip()))
    else:
      fresh_id_ranges.append(list(map(int, line.strip().split('-'))))

# print(part1(*sample_data))
# print(part1(fresh_id_ranges, ingredient_ids))


'''
--- Part Two ---
The Elves start bringing their spoiled inventory to the trash chute at the back of the kitchen.

So that they can stop bugging you when they get new inventory, the Elves would like to know all of the IDs that the fresh ingredient ID ranges consider to be fresh. An ingredient ID is still considered fresh if it is in any range.

Now, the second section of the database (the available ingredient IDs) is irrelevant. Here are the fresh ingredient ID ranges from the above example:

3-5
10-14
16-20
12-18
The ingredient IDs that these ranges consider to be fresh are 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, and 20. So, in this example, the fresh ingredient ID ranges consider a total of 14 ingredient IDs to be fresh.

Process the database file again. How many ingredient IDs are considered to be fresh according to the fresh ingredient ID ranges?
'''

def part2(ids: list[list[int]]) -> int:
  ids.sort()

  prev_start = 0
  tot = 0
  for start, end in ids:
    prev_start = max(prev_start, start)
    if prev_start <= end:
      tot += end - prev_start + 1
    prev_start = max(prev_start, end + 1)

  return tot

print(part2(fresh_id_ranges))
