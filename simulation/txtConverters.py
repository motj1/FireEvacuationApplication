from Position import Position
from Tile import *
import re
from time import sleep
import fcntl
import os

# Parse a .txt file into an w x h array of tiles corresponding to the w x h map given inside
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
      if c == 'P':
        agents.append(Position(i, j))
        buildingMap[i][j] = createTile(' ', True)
      else:
        buildingMap[i][j] = createTile(c, False)
      c = f.read(1)
      j += 1
    c = f.read(1)
    i += 1
      
  return buildingMap, dimensions, agents

# Parse the map array of tiles, m, into a text file to be printed
def generateFile(m, w, h):
  with open("map.txt", "r") as f:
      fcntl.flock(f.fileno(), fcntl.LOCK_EX)
      sleep(0.5)
  with open("map.txt", "w") as f:
    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
    for i in range(h):
      for j in range(w):
        if (m[i][j].hasAgent == True):
          f.write("P")
        else:
          f.write(parseChar(m[i][j].kind))
      f.write("\n")
  return "map.txt"

# Block access to map.txt for a given amount of time
def blockFile(blockTime):
  with open("map.txt", "r") as f:
    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
    sleep(blockTime)

# Given the kind of a tile, return the appropriate representative character
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

# Generates the map.txt based on the simulation state and prints its contents to terminal
def printMap(m, w, h):
  generateFile(m, w, h)
  print(open("map.txt").read())