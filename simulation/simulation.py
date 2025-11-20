import sys
from algorithm import *
from Position import *
from txtConverters import *
from Agent import *
from txtConverters import *
from Smoke import *
import random
from tabulate import tabulate
import time

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
