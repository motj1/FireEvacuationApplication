import sys
from algorithm import *
from Position import *
from txtConverters import *
from Agent import *
from txtConverters import *
import time
import random

def spreadFire(m, dims):
  tilesSpreadTo = [];

  for i in range(len(dims)):
    for j in range(dims[i][0]):
      for k in range(dims[i][1]):
        if m[i][j][k].kind == "fire":
          adjacencyCoords = [[0, 1], [1, 0], [0, -1], [-1, 0], [-1, -1], [1, 1], [-1, 1], [1, -1]]

          for coord in adjacencyCoords:
            row = j + coord[0]
            col = k + coord[1]

            if m[i][row][col].isBurnable() and spreadHappens():
              tilesSpreadTo.append(m[i][row][col])

          if type(m[i][j][k]) is Stairwell:
            if (m[i][j][k].down.row >= 0):
              d = m[i][j][k].down
              downCell = m[d.floor][d.row][d.col]
              if downCell.isBurnable() and spreadHappens():
                tilesSpreadTo.append(m[d.floor][d.row][d.col])

  for tile in tilesSpreadTo:
    tile.kind = "fire"

def spreadHappens():
  return random.randint(1, 8) <= 1

# waitForResponse()

# time.sleep(0.5)``
m, dims, a = generateMultiStoryMapStairs(sys.argv[1])
printMultiStoryMap(m, dims)

# Generate the instruction sets for each agent using the algorithm being tested
agentInstructions = []

for i in range(len(a)):
  agentInstructions.append(bfs3D(m, a[i], dims))

tick = 0
trapped = 0
finished = [False for _ in range(len(a))]
while 1:
  nextInstructions = []

  spreadFire(m, dims)

  for i in range(len(a)):
    if finished[i] == True:
      nextInstructions.append(Position3D(-1, -1, -1))
      continue
    nextInstruction = bfs3D(m, a[i], dims)

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

print(f"Simulation completed in {tick} ticks!")
if trapped == 1:
  print(f"There was {trapped} person trapped")
else:
  print(f"There were {trapped} people trapped")
if len(a) - trapped == 1:
  print(f"{len(a) - trapped} person escaped")
else:
  print(f"{len(a) - trapped} people escaped")
blockFile(10)
