from Position import *
from Tile import *
import re
from time import sleep
import fcntl

def generateMultiStoryFile(m, dims):
  maximumHeight = -1
  
  for i in range(len(dims)):
    if dims[i][0] > maximumHeight:
      maximumHeight = dims[i][0]

  # sleep(0.01)
  # with open("map.txt", "r") as f:
  #   fcntl.flock(f.fileno(), fcntl.LOCK_EX)
  #   sleep(0.05)
  #   fcntl.flock(f, fcntl.LOCK_UN)
  sleep(0.20)
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
          if m[j][i][k].kind == "fire":
            f.write("F")
          elif (m[j][i][k].hasAgent == True):
            f.write("P")
          else:
            f.write(parseChar(m[j][i][k].kind))
        f.write("     ")
      f.write("\n")

    fcntl.flock(f, fcntl.LOCK_UN)
  # waitForResponse()

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
  elif kind == "internal_wall":
    return '|'
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
  elif kind == 'strs':
    return 'S'
  elif kind == 'door':
    return 'd'
  elif kind == 'frdr':
    return 'D'
  elif kind == "err":  
    return '?'

def printMultiStoryMap(m, dims):
  generateMultiStoryFile(m, dims)
  print(open("map.txt").read())

def generateMultiStoryMapStairs(filename):
  f = open(filename)

  agents = []

  numFloors = readFileForNumbers(f, 1)

  buildingMap = []
  floorDimensions = []

  for i in range(numFloors[0]):
    floorDimensions.append(readFileForNumbers(f, 2))
    numStairs = readFileForNumbers(f, 1)

    stairMappings = []
    for j in range(numStairs[0]):
      stairMappings.append(readFileForNumbers(f, 1))

    buildingMap.append([[Tile() for _ in range(floorDimensions[i][1])] for _ in range(floorDimensions[i][0])])

    stairNumber = 0

    for j in range(floorDimensions[i][0]):
      for k in range(floorDimensions[i][1]+1):
        c = f.read(1)
        if c == 'P':
          agents.append(Position3D(i, j, k))
          buildingMap[i][j][k] = Tile(parseKind(' '), 10, True)
        elif c == 'S':
          fDown = stairMappings[stairNumber][0]
          rDown = stairMappings[stairNumber][1]
          cDown = stairMappings[stairNumber][2]
          fUp = stairMappings[stairNumber][3]
          rUp = stairMappings[stairNumber][4]
          cUp = stairMappings[stairNumber][5]

          buildingMap[i][j][k] = Stairwell(parseKind('S'), 10, False, Position3D(fUp, rUp, cUp), Position3D(fDown, rDown, cDown))
          stairNumber += 1
        elif c == '\n':
          break
        else:
          buildingMap[i][j][k] = Tile(parseKind(c), 10, False)
    c = f.read(1) 

  return buildingMap, floorDimensions, agents

def readFileForNumbers(f, n):
  firstLine = [next(f) for _ in range(n)]
  text = "".join(firstLine)
  return [int(n) for n in re.findall(r'-?\d+', text)]

def printWaitGraph(m, wg, dims, f):
  for j in range(dims[f][0]):
    for k in range(dims[f][1]):
      if m[f][j][k].kind == 'wall':
        print('#',end='')
      elif wg[f][j][k] == 0:
        print(' ',end='')
      else:
        print(wg[f][j][k], end='')
    print('')

def generateFileWithWaits(m, wg, dims):
  maximumHeight = -1
  
  for i in range(len(dims)):
    if dims[i][0] > maximumHeight:
      maximumHeight = dims[i][0]

  # sleep(0.01)
  # with open("map.txt", "r") as f:
  #   fcntl.flock(f.fileno(), fcntl.LOCK_EX)
  #   sleep(0.05)
  #   fcntl.flock(f, fcntl.LOCK_UN)
  sleep(0.20)
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
          if m[j][i][k].kind != "fire" and  m[j][i][k].kind != "door" and  m[j][i][k].kind != "frdr" and  m[j][i][k].kind != "void":
            f.write(parseChar(m[j][i][k].kind))
          elif (wg[j][i][k] != 0):
            f.write(str(wg[j][i][k]))
          else:
            f.write(' ')
        f.write("     ")
      f.write("\n")

    fcntl.flock(f, fcntl.LOCK_UN)
  # waitForResponse()

  return "map.txt"
