from Position import Position
from Tile import *
import re
from time import sleep
import fcntl
import os

def generateMap(filename):
  f = open(filename)

  agents = []

  first_two_lines = [next(f) for _ in range(2)]
  text = "".join(first_two_lines)
  dimensions = [int(n) for n in re.findall(r'-?\d+', text)]
  print(dimensions)

  buildingMap = [[Tile() for _ in range(dimensions[0])] for _ in range(dimensions[1])]

  i = 0
  c = f.read(1)
  while c != '':
    j = 0
    while c != '\n':
      buildingMap[i][j] = createTile(c)
      if c == 'P':
        agents.append(Position(i, j))
      c = f.read(1)
      j += 1
    c = f.read(1)
    i += 1
      
  return buildingMap, dimensions, agents

def generateFile(m, w, h):
  with open("map.txt", "r") as f:
      fcntl.flock(f.fileno(), fcntl.LOCK_EX)
      sleep(0.5)
  with open("map.txt", "w") as f:
    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
    for i in range(h):
      for j in range(w):
        f.write(parseChar(m[i][j].kind))
      f.write("\n")
  return "map.txt"

def blockFile(blockTime):
  with open("map.txt", "r") as f:
    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
    sleep(blockTime)

def parseChar(kind):
  if kind == "wall":
    return '#'
  elif kind == "void":
    return ' '
  elif kind == "fire":
    return 'F'
  elif kind == 'obst':
    return 'O'
  elif kind == "exit":
    return 'E'
  elif kind == "prsn":
    return 'P'
  elif kind == "path":
    return '+'
  elif kind == "err":  
    return '?'