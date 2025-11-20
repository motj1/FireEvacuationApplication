import sys
from algorithm import *
from Position import *
from txtConverters import *
from Agent import *
from txtConverters import *
import random
from tabulate import tabulate
import time

# spreads fire and smoke
def spreadFire(m, dims):
  fireSpreadTiles = []

  for i in range(len(dims)):
    for j in range(dims[i][0]):
      for k in range(dims[i][1]):
        curTile = m[i][j][k]
        if curTile.kind == "fire":
          adjacencyCoords = [[0, 1], [1, 0], [0, -1], [-1, 0], [-1, -1], [1, 1], [-1, 1], [1, -1]]

          for coord in adjacencyCoords:
            row = j + coord[0]
            col = k + coord[1]
            destTile = m[i][row][col]

            if canFireSpread(curTile, destTile):
              fireSpreadTiles.append(destTile)

          if type(curTile) is Stairwell:
            if (curTile.down.row >= 0):
              d = curTile.down
              downCell = m[d.floor][d.row][d.col]
              if canFireSpread(curTile, downCell):
                fireSpreadTiles.append(m[d.floor][d.row][d.col])
            if (curTile.up.row >= 0):
              u = curTile.up
              upCell = m[u.floor][u.row][u.col]
              if canFireSpread(curTile, upCell):
                fireSpreadTiles.append(m[u.floor][u.row][u.col])

  for tile in fireSpreadTiles:
    tile.kind = "fire"
    print("fire")

def spreadSmoke(m, dims):
  smokeSpreadTiles = []

  for i in range(len(dims)):
    for j in range(dims[i][0]):
      for k in range(dims[i][1]):
        curTile = m[i][j][k]
        # iterate through fire and smoke1-4 nodes to spread smoke as smoke1-5
        if curTile.kind in ["fire"] + [f"smoke{i}" for i in range(1,6)]:
          adjacencyCoords = [[0, 1], [1, 0], [0, -1], [-1, 0], [-1, -1], [1, 1], [-1, 1], [1, -1]]

          for coord in adjacencyCoords:
            row = j + coord[0]
            col = k + coord[1]
            destTile = m[i][row][col]

            if canSmokeSpread(curTile, destTile):
              smokeSpreadTiles.append((destTile, getGradientSmoke(curTile)))

          if type(curTile) is Stairwell:
            if (curTile.down.row >= 0):
              d = curTile.down
              downCell = m[d.floor][d.row][d.col]
              if canSmokeSpread(curTile, downCell):
                smokeSpreadTiles.append((downCell, getGradientSmoke(curTile)))
            if (curTile.up.row >= 0):
              u = curTile.up
              upCell = m[u.floor][u.row][u.col]
              if canSmokeSpread(curTile, upCell):
                smokeSpreadTiles.append((upCell, getGradientSmoke(curTile)))

  for tile, newKind in smokeSpreadTiles: 
    if tile.kind[0:5] == "smoke" and tile.kind[5] < newKind[5]:
      continue
    tile.kind = newKind

# fire can only spread off other fire tiles
def canFireSpread (sourceTile: Tile, destTile: Tile):
  return sourceTile.kind == "fire" and destTile.isBurnable() and spreadHappens()

# smoke can spread off fire and smoke tiles, but cannot spread to fire
def canSmokeSpread (sourceTile: Tile, destTile: Tile) -> bool:
  if destTile.kind in ["fire", "exit"] or not destTile.isTraversable():
    return False

  # if destTile isn't fire and sourceTile is fire, then smoke can always spread
  if sourceTile.kind == "fire":
    return True
  elif sourceTile.kind[0:5] == "smoke":
    if not smokeSpreadHappens(int(sourceTile.kind[5])):
      return False
    if destTile.kind[0:5] == "smoke":
      return int(sourceTile.kind[5]) > int(destTile.kind[5])
    else:
      return True
  else:
    return False
  
def getGradientSmoke(sourceTile: Tile) -> str:
  if sourceTile.kind == "fire":
    return "smoke1"
  else:
    return "smoke" + str(int(sourceTile.kind[5])+1)

def spreadHappens():
  return random.randint(1, 8) <= 1

def smokeSpreadHappens (sourceIntensity: int) -> bool:
  # smoke chance is proportional to intensity
  return random.randint(1, (sourceIntensity+2)//3) <= 1

# waitForResponse()

# time.sleep(0.5)
m, dims, a = generateMultiStoryMapStairs(sys.argv[1])
printMultiStoryMap(m, dims)

# Generate the instruction sets for each agent using the algorithm being tested
agentInstructions = []

for i in range(len(a)):
  agentInstructions.append(astar(m, a[i], dims))# bfs3D(m, a[i], dims))

tick = 0
trapped = 0
finished = [False for _ in range(len(a))]
while 1:
  nextInstructions = []

  spreadFire(m, dims)
  spreadSmoke(m, dims)

  for i in range(len(a)):
    if finished[i] == True:
      nextInstructions.append(Position3D(-1, -1, -1))
      continue
    nextInstruction = astar(m, a[i], dims) #bfs3D(m, a[i], dims) #

    if nextInstruction.floor == -1:
      trapped += 1
      finished[i] = True
      nextInstructions.append(Position3D(-1, -1, -1))
    else:
      nextInstructions.append(nextInstruction)

  # Loop through all agents and move them according to 
  for i in range(len(a)):
    if finished[i] == True:
      continue
    
    # Attempt to move the agent
    moved, a[i] = moveAgent3D(m, a[i], nextInstructions[i])

  # Remove an agent that has reached an exit tile from that tile
  for agent in reversed(a):
    if m[agent.floor][agent.row][agent.col].kind == "exit":
      m[agent.floor][agent.row][agent.col].hasAgent = False
      finished[a.index(agent)] = True

  printMultiStoryMap(m, dims)

  numAgentsFinished = 0
  for i in range(len(finished)):
    if finished[i] == True:
      numAgentsFinished += 1

  if len(a) == numAgentsFinished:
    break

  tick += 1

data = [
    ["Evacuated", len(a) - trapped],
    ["Trapped", trapped],
]
headers = ["Status", "# People"]
print(tabulate(data, headers=headers, tablefmt="fancy_grid"))
print(f"Simulation finished in {tick} tick(s)!")
