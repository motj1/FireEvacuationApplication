import sys
from algorithm import *
from Position import *
from txtConverters import *
from Agent import *
from txtConverters import *
import time

m, dims, a = generateMultiStoryMap(sys.argv[1])
printMultiStoryMap(m, dims)

# Generate the instruction sets for each agent using the algorithm being tested
agentInstructions = []

for i in range(len(a)):
  agentFloor = a[i].floor
  agentInstructions.append(bfs(m[agentFloor], a[i], dims[agentFloor][1], dims[agentFloor][0]))

tick = 0
while 1:
  numAgentsFinished = 0

  # Loop through all agents and move them according to 
  for i in range(len(a)):
    agentFloor = a[i].floor

    if (tick >= len(agentInstructions[i])):
      numAgentsFinished += 1
      continue
    
    # Attempt to move the agent
    moved, a[i] = moveAgent3D(m[agentFloor], agentFloor, a[i], agentInstructions[i][tick])

    # Insert a buffer instruction to stop the agent from moving past the current instruction
    if moved == False:
      agentInstructions[i].insert(tick, Position(-1,-1)) 
  
  printMultiStoryMap(m, dims)

  # Remove an agent that has reached an exit tile from that tile
  for agent in reversed(a):
    if m[agent.floor][agent.row][agent.col].kind == "exit":
      m[agent.floor][agent.row][agent.col].hasAgent = False

  if len(a) == numAgentsFinished:
    break
  tick += 1
  time.sleep(0.5)

print(f"Simulation completed in {tick} ticks!")