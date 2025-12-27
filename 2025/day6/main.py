'''
--- Day 6: Trash Compactor ---
After helping the Elves in the kitchen, you were taking a break and helping them re-enact a movie scene when you over-enthusiastically jumped into the garbage chute!

A brief fall later, you find yourself in a garbage smasher. Unfortunately, the door's been magnetically sealed.

As you try to find a way out, you are approached by a family of cephalopods! They're pretty sure they can get the door open, but it will take some time. While you wait, they're curious if you can help the youngest cephalopod with her math homework.

Cephalopod math doesn't look that different from normal math. The math worksheet (your puzzle input) consists of a list of problems; each problem has a group of numbers that need to be either added (+) or multiplied (*) together.

However, the problems are arranged a little strangely; they seem to be presented next to each other in a very long horizontal list. For example:

123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
Each problem's numbers are arranged vertically; at the bottom of the problem is the symbol for the operation that needs to be performed. Problems are separated by a full column of only spaces. The left/right alignment of numbers within each problem can be ignored.

So, this worksheet contains four problems:

123 * 45 * 6 = 33210
328 + 64 + 98 = 490
51 * 387 * 215 = 4243455
64 + 23 + 314 = 401
To check their work, cephalopod students are given the grand total of adding together all of the answers to the individual problems. In this worksheet, the grand total is 33210 + 490 + 4243455 + 401 = 4277556.

Of course, the actual worksheet is much wider. You'll need to make sure to unroll it completely so that you can read the problems clearly.

Solve the problems on the math worksheet. What is the grand total found by adding together all of the answers to the individual problems?


'''
import re # regular expression lib

sample_data = [
  '123 328  51 64 ',
  ' 45 64  387 23 ',
  '  6 98  215 314',
  '*   +   *   +  '
]

def parse_input(data: list[str]) -> tuple[list[list[int]], list[str]]:
  '''
  Parse input string to list of math operands (by column) and list of operators (operators[i] is the operator used to calculate the final result of operands[i])
  
  :param data: input string, each line contains numbers separated by spaces, except the last line is either * or +
  :type data: list[str]
  :return: tuple[operands, operators]
  :rtype: tuple[list[list[int]], list[str]]
  '''

  operators = re.split(r'\s+', data[-1])

  m, n = len(data), len(operators)
  operands = [[None] * (m - 1) for _ in range(n)]

  for i, line in enumerate(data):
    if i == m - 1:
      break

    for j, value in enumerate(re.split(r'\s+', line)):
      operands[j][i] = int(value)

  return (operands, operators)

def calc(lhs: int, rhs: int, op: str) -> int:
  if op == '*':
    return lhs * rhs
  
  return lhs + rhs

def part1(operands: list[list[int]], operators: list[str]) -> int:
  tot = 0

  for i, nums in enumerate(operands):
    curr = nums[0]

    for j in range(1, len(nums)):
      curr = calc(curr, nums[j], operators[i])

    tot += curr

  return tot

# print(
#   part1(*parse_input(sample_data))
# )

import os

data = []

with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as file:
  for line in file.readlines():
    data.append(line.strip())

# print(
#   part1(*parse_input(data))
# )  

'''
--- Part Two ---
The big cephalopods come back to check on how things are going. When they see that your grand total doesn't match the one expected by the worksheet, they realize they forgot to explain how to read cephalopod math.

Cephalopod math is written right-to-left in columns. Each number is given in its own column, with the most significant digit at the top and the least significant digit at the bottom. (Problems are still separated with a column consisting only of spaces, and the symbol at the bottom of the problem is still the operator to use.)

Here's the example worksheet again:

123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
Reading the problems right-to-left one column at a time, the problems are now quite different:

The rightmost problem is 4 + 431 + 623 = 1058
The second problem from the right is 175 * 581 * 32 = 3253600
The third problem from the right is 8 + 248 + 369 = 625
Finally, the leftmost problem is 356 * 24 * 1 = 8544
Now, the grand total is 1058 + 3253600 + 625 + 8544 = 3263827.

Solve the problems on the math worksheet again. What is the grand total found by adding together all of the answers to the individual problems?
'''

def part2(data: list[str]) -> int:
  operators: list[tuple[str, int, int]] = [] # (operator, start column, end column)

  m, n = len(data), len(data[-1])

  prev = -1
  for j, char in enumerate(data[-1]):
    if char == '+' or char == '*':
      if prev >= 0:
        operators.append((data[-1][prev], prev, j - 2))

      prev = j

  if prev >= 0:
    operators.append((data[-1][prev], prev, n - 1))

  tot = 0
  for op, start, end in operators:
    prev = None

    for j in range(end, start - 1, -1):
      curr = 0
      for i in range(m - 1):
        if data[i][j] != ' ':
          curr = curr * 10 + int(data[i][j])

      if prev is None:
        prev = curr
      else:
        prev = calc(prev, curr, op)

    tot += prev

  return tot

print(part2(data))

