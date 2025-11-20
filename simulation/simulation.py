import sys
from algorithm import *
from Position import *
from txtConverters import *
from Agent import *
from txtConverters import *
from tabulate import tabulate
import time
from fire import *

if (len(sys.argv) > 2):
  printPython = 0
else:
  printPython = 1

if (not printPython):
  waitForResponse()

  time.sleep(1)
m, dims, a = generateMultiStoryMapStairs(sys.argv[1])

printMultiStoryMap(m, dims, printPython)

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

while 1:
  time.sleep(0.1)
  nextInstructions = []

  spreadFire(m, dims, 1)
  
  cell_details = calculate_dests(m, dims)
  # depth_maps = getPredictiveMaps(m, dims, 3, 2)

  for i in range(len(a)):
    if finished[i] == True:
      nextInstructions.append(Position3D(-1, -1, -1))
      continue
    nextInstruction = nextmove(a[i], cell_details) #bfsPredictive(m, depth_maps, a[i], dims) bfs3D(m, a[i], dims) astar(m, a[i], dims)   

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

  printMultiStoryMap(m, dims, printPython)

  numAgentsFinished = 0
  for i in range(len(finished)):
    if finished[i] == True:
      numAgentsFinished += 1

  if len(a) == numAgentsFinished:
    break

  tick += 1

printWaitGraph(m, waitGraph, dims, 0)
generateFileWithWaits(m, waitGraph, dims)

data = [
    ["Evacuated", len(a) - trapped],
    ["Trapped", trapped],
]
headers = ["Status", "# People"]
print(tabulate(data, headers=headers, tablefmt="fancy_grid"))
print(f"Simulation finished in {tick} tick(s)!")
