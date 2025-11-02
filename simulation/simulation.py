import sys
from algorithm import *
from Position import *
from txtConverters import *
from Agent import *
from txtConverters import *

# Read in input map 
m, dims, a = generateMap(sys.argv[1])
w = dims[0]
h = dims[1]
printMap(m, w, h)

# Generate the instruction sets for each agent using the algorithm being tested
agentInstructions = []
for i in range(len(a)):
  agentInstructions.append(bfs(m, a[i], w, h))

tick = 0
while 1:
  numAgentsFinished = 0

  # Loop through all agents and move them according to 
  for i in range(len(a)):
    if (tick >= len(agentInstructions[i])):
      numAgentsFinished += 1
      continue
    
    # Attempt to move the agent
    moved, a[i] = moveAgent(m, a[i], agentInstructions[i][tick])

    # Insert a buffer instruction to stop the agent from moving past the current instruction
    if moved == False:
      agentInstructions[i].insert(tick, Position(-1,-1)) 
  
  printMap(m, w, h)

  # Remove an agent that has reached an exit tile from that tile
  for agent in reversed(a):
    if m[agent.row][agent.col].kind == "exit":
      m[agent.row][agent.col].hasAgent = False

  if len(a) == numAgentsFinished:
    break
  tick += 1

print(f"Simulation completed in {tick} ticks!")