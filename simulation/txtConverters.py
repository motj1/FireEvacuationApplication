from Position import *
from Tile import *
import re
from time import sleep
import fcntl

# Parse a .txt file into an w x h array of tiles corresponding to the w x h map given inside
def generateMap(filename):
  f = open(filename)

  agents = []

  first_two_lines = [next(f) for _ in range(2)]
  text = "".join(first_two_lines)
  dimensions = [int(n) for n in re.findall(r'-?\d+', text)]
  print(dimensions)

  buildingMap = [[Tile() for _ in range(dimensions[1])] for _ in range(dimensions[0])]

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

def generateMultiStoryMap(filename):
  f = open(filename)

  agents = []

  firstLine = [next(f) for _ in range(1)]
  text = "".join(firstLine)
  numFloors = [int(n) for n in re.findall(r'-?\d+', text)]

  buildingMap = []
  floorDimensions = []

  print(numFloors)

  for i in range(numFloors[0]):
    twoLines = [next(f) for _ in range(2)]
    text = "".join(twoLines)
    
    floorDimensions.append([int(n) for n in re.findall(r'-?\d+', text)])

    print(floorDimensions[i])

    buildingMap.append([[Tile() for _ in range(floorDimensions[i][1])] for _ in range(floorDimensions[i][0])])

    for j in range(floorDimensions[i][0]):
      for k in range(floorDimensions[i][1] + 1):
        c = f.read(1)
        if c == 'P':
          agents.append(Position3D(i, j, k))
          buildingMap[i][j][k] = createTile(' ', True)
        elif c == '\n':
          break
        else:
          buildingMap[i][j][k] = createTile(c, False)
    c = f.read(1) 
  return buildingMap, floorDimensions, agents

# Parse the map array of tiles, m, into a text file to be printed
def generateFile(m, h, w):
  with open("map.txt", "w") as f:
    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
    for i in range(h):
      for j in range(w):
        if (m[i][j].hasAgent == True):
          f.write("P")
        else:
          f.write(parseChar(m[i][j].kind))
      f.write("\n")
    fcntl.flock(f, fcntl.LOCK_UN)
  return "map.txt"

def generateMultiStoryFile(m, dims):
  maximumHeight = -1
  
  for i in range(len(dims)):
    if dims[i][0] > maximumHeight:
      maximumHeight = dims[i][0]

  with open("map.txt", "r") as f:
    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
    sleep(0.5)
    fcntl.flock(f, fcntl.LOCK_UN)
  with open("map.txt", "w") as f:
    fcntl.flock(f.fileno(), fcntl.LOCK_EX)

    totalx = 0
    maxy = 0
    for i in range(len(dims)):
      totalx += dims[i][1] + 5
      if (dims[i][0] >= maxy): 
        maxy = dims[i][0] + 1
    f.write(f"{totalx} {maxy}\n")

    for j in range(len(dims)):
      for k in range(dims[j][1]):
        if k == 0:
          f.write("F")
        elif k == 1:
          f.write(f"{j}")
        else:
          f.write(" ")
      f.write("     ")
    f.write("\n")

    for i in range(maximumHeight):
      for j in range(len(dims)):
        if i >= dims[j][0]:
          for k in range(dims[j][1]):
            f.write(" ")
          f.write("     ")
          continue
        for k in range(dims[j][1]):
          if (m[j][i][k].hasAgent == True):
            f.write("P")
          else:
            f.write(parseChar(m[j][i][k].kind))
        f.write("     ")
      f.write("\n")

    fcntl.flock(f, fcntl.LOCK_UN)


  return "map.txt"


# Block access to map.txt for a given amount of time
def blockFile(blockTime):
  with open("map.txt", "r") as f:
    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
    sleep(blockTime)
    fcntl.flock(f, fcntl.LOCK_UN)

def waitForResponse():
  with open("map.txt", "r+") as f:
    while True:
      try:
          fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
          sleep(0.01)
          fcntl.flock(f, fcntl.LOCK_UN)
      except BlockingIOError:
          break

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
def printMap(m, h, w):
  generateFile(m, h, w)
  print(open("map.txt").read())

def printMultiStoryMap(m, dims):
  generateMultiStoryFile(m, dims)
  print(open("map.txt").read())