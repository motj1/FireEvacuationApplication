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
from fire import *

algos = ["bfs", "bfsPred", "astar", "nextMove"]
algo = sys.argv[1]

if algo not in algos:
  print("Please choose a valid algorithm")
  exit()

m, dims, a = generateMultiStoryMapStairs(sys.argv[2])

printMultiStoryMap(m, dims, True)

waitGraph = []
for i in range(len(dims)):
  waitGraph.append([[0 for _ in range(dims[i][1])] for _ in range(dims[i][0])])

# Generate the instruction sets for each agent using the algorithm being tested
# agentInstructions = []

# for i in range(len(a)):
#   agentInstructions.append(astar(m, a[i], dims))# bfs3D(m, a[i], dims))

tick = 0
trapped = 0
finished = [False for _ in range(len(a))]

time.sleep(2)

while 1:
  time.sleep(0.1)
  nextInstructions = []

  spreadFire(m, dims, 0.1)
  spreadSmoke(m, dims)

  if algo == "nextMove":
    cell_details = calculate_dests(m, dims)
  elif algo == "bfsPred":
    depth_maps = getPredictiveMaps(m, dims, 3, 2)

  for i in range(len(a)):
    if finished[i] == True:
      nextInstructions.append(Position3D(-1, -1, -1))
      continue
    if algo == "bfs":
      nextInstruction = bfs3D(m, a[i], dims)
    elif algo == "bfsPred":
      nextInstruction = bfsPredictive(m, depth_maps, a[i], dims)
    elif algo == "astar":
      nextInstruction = astar(m, a[i], dims) 
    elif algo == "nextMove":
      nextInstruction = nextmove(a[i], cell_details)

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

    if moved == False and waitGraph[a[i].floor][a[i].row][a[i].col] < 9:
      waitGraph[a[i].floor][a[i].row][a[i].col] += 1

  # Remove an agent that has reached an exit tile from that tile
  for agent in reversed(a):
    if m[agent.floor][agent.row][agent.col].kind == "exit":
      m[agent.floor][agent.row][agent.col].hasAgent = False
      finished[a.index(agent)] = True

  printMultiStoryMap(m, dims, True)

  numAgentsFinished = 0
  for i in range(len(finished)):
    if finished[i] == True:
      numAgentsFinished += 1

  if len(a) == numAgentsFinished:
    break

  tick += 1

printWaitGraph(m, waitGraph, dims, 0)
generateFileWithWaits(m, waitGraph, dims)
print(f"Total Wait Value = {getTotalWait(waitGraph, dims)}")

data = [
    ["Evacuated", len(a) - trapped],
    ["Trapped", trapped],
]
headers = ["Status", "# People"]
print(tabulate(data, headers=headers, tablefmt="fancy_grid"))
print(f"Simulation finished in {tick} tick(s)!")
