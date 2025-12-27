'''
--- Day 11: Reactor ---
You hear some loud beeping coming from a hatch in the floor of the factory, so you decide to check it out. Inside, you find several large electrical conduits and a ladder.

Climbing down the ladder, you discover the source of the beeping: a large, toroidal reactor which powers the factory above. Some Elves here are hurriedly running between the reactor and a nearby server rack, apparently trying to fix something.

One of the Elves notices you and rushes over. "It's a good thing you're here! We just installed a new server rack, but we aren't having any luck getting the reactor to communicate with it!" You glance around the room and see a tangle of cables and devices running from the server rack to the reactor. She rushes off, returning a moment later with a list of the devices and their outputs (your puzzle input).

For example:

aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
Each line gives the name of a device followed by a list of the devices to which its outputs are attached. So, bbb: ddd eee means that device bbb has two outputs, one leading to device ddd and the other leading to device eee.

The Elves are pretty sure that the issue isn't due to any specific device, but rather that the issue is triggered by data following some specific path through the devices. Data only ever flows from a device through its outputs; it can't flow backwards.

After dividing up the work, the Elves would like you to focus on the devices starting with the one next to you (an Elf hastily attaches a label which just says you) and ending with the main output to the reactor (which is the device with the label out).

To help the Elves figure out which path is causing the issue, they need you to find every path from you to out.

In this example, these are all of the paths from you to out:

Data could take the connection from you to bbb, then from bbb to ddd, then from ddd to ggg, then from ggg to out.
Data could take the connection to bbb, then to eee, then to out.
Data could go to ccc, then ddd, then ggg, then out.
Data could go to ccc, then eee, then out.
Data could go to ccc, then fff, then out.
In total, there are 5 different paths leading from you to out.

How many different paths lead from you to out?



--- Part Two ---
Thanks in part to your analysis, the Elves have figured out a little bit about the issue. They now know that the problematic data path passes through both dac (a digital-to-analog converter) and fft (a device which performs a fast Fourier transform).

They're still not sure which specific path is the problem, and so they now need you to find every path from svr (the server rack) to out. However, the paths you find must all also visit both dac and fft (in any order).

For example:

svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
This new list of devices contains many paths from svr to out:

svr,aaa,fft,ccc,ddd,hub,fff,ggg,out
svr,aaa,fft,ccc,ddd,hub,fff,hhh,out
svr,aaa,fft,ccc,eee,dac,fff,ggg,out
svr,aaa,fft,ccc,eee,dac,fff,hhh,out
svr,bbb,tty,ccc,ddd,hub,fff,ggg,out
svr,bbb,tty,ccc,ddd,hub,fff,hhh,out
svr,bbb,tty,ccc,eee,dac,fff,ggg,out
svr,bbb,tty,ccc,eee,dac,fff,hhh,out
However, only 2 paths from svr to out visit both dac and fft.

Find all of the paths that lead from svr to out. How many of those paths visit both dac and fft?
'''

import os
from collections import defaultdict
from functools import cache

sample_data = [
  'aaa: you hhh',
  'you: bbb ccc', # <-- starting point
  'bbb: ddd eee',
  'ccc: ddd eee fff',
  'ddd: ggg',
  'eee: out',
  'fff: out',
  'ggg: out',
  'hhh: ccc fff iii',
  'iii: out'
]

sample_data2 = [
  'svr: aaa bbb',
  'aaa: fft',
  'fft: ccc',
  'bbb: tty',
  'tty: ccc',
  'ccc: ddd eee',
  'ddd: hub',
  'hub: fff',
  'eee: dac',
  'dac: fff',
  'fff: ggg hhh',
  'ggg: out',
  'hhh: out'
]

def part1(devices: list[str], outputs: list[list[str]]):
  '''
  Counts number of way to connect from 'you' to 'out' using the list of devices and their outputs.
  It's guaranteed to have at least one device named 'you'

  Paramters:
    devices (list[str]): List of device names
    outputs (list[list[str]]): List of outputs from each devices. outputs[i] = list of output of devices[i]
  '''

  g = defaultdict(list[str]) # adjacency list
  for i, device in enumerate(devices):
    for out_device in outputs[i]:
      g[device].append(out_device)
  
  @cache
  def dfs(curr_device: str) -> int:
    if curr_device == 'out':
      return 1
    
    tot = 0
    for out_device in g[curr_device]:
      tot += dfs(out_device)

    return tot
  
  print('part1', dfs('you'))

def part2(devices: list[str], outputs: list[list[str]]):
  '''
  Counts number of ways to connect from 'svr' (the server rack) to 'out',
    in which the paths must visit both 'dac' (a digital-to-analog converter)
      and 'fft' (ad fast fourier transform) in any order

  Paramters:
    devices (list[str]): List of device names
    outputs (list[list[str]]): List of outputs from each devices. outputs[i] = list of output of devices[i]
  '''

  g = defaultdict(dict[str, bool]) # adjacency list
  for i, device in enumerate(devices):
    for out_device in outputs[i]:
      g[device][out_device] = 1

  @cache
  def dfs(curr_device: str, dac: int, fft: int) -> int:
    # print(f'curr_device={curr_device}, dac={dac}, fft={fft}')
    if curr_device == 'out':
      return 1 if dac == 1 and fft == 1 else 0
    
    tot = 0
    for out_device in g[curr_device]:
      next_dac = 1 if out_device == 'dac' else dac
      next_fft = 1 if out_device == 'fft' else fft
      tot += dfs(out_device, next_dac, next_fft)

    return tot
  
  print('part2', dfs('svr', 0, 0))

def main():
  # Preprocess data
  data = []
  devices = []
  outputs = []

  with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as file:
    for line in file.readlines():
      data.append(line.strip())

  for line in data:
    device_name, output = line.split(': ')
    devices.append(device_name)
    outputs.append(output.split(' '))

  # part1(devices, outputs)
  part2(devices, outputs)

if __name__ == '__main__':
  main()
