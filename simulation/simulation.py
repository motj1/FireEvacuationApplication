import sys
from algorithm import *
from Position import *
from txtConverters import *
from Agent import *
from txtConverters import *
import time

def printMapData(m, w, h):
  for i in range(w):
    for j in range(h):
      print(f"({m[i][j].kind} {m[i][j].hp})", end=" ")
    print("\n")

def printMap(m, w, h):
  generateFile(m, w, h)
  print(open("map.txt").read())

# MAIN FUNCTION
time.sleep(2)
m, dims, a = generateMap(sys.argv[1])
w = dims[0]
h = dims[1]
printMap(m, w, h)
blockFile(5)

for i in range(len(a)):
  prev, firstExit = bfsAgent(m, a[i], w, h)
  drawPath(m, firstExit, prev)
  printMap(m, w, h)


printMap(m, w, h)

while 1:
  blockFile(10)