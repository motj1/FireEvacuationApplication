from Position import *
  
def moveAgent3D(m, agentPos, agentInstructions):
  newFloor = agentInstructions.floor
  newRow = agentInstructions.row
  newCol = agentInstructions.col

  if newFloor != agentPos.floor and m[newFloor][newRow][newCol].hasAgent == False:
    m[agentPos.floor][agentPos.row][agentPos.col].hasAgent = False
    m[newFloor][newRow][newCol].hasAgent = True
    return [True, Position3D(newFloor, newRow, newCol)]

  if abs(agentPos.col - newCol) <= 1 and abs(agentPos.row - newRow) <= 1 and m[newFloor][newRow][newCol].isTraversable() and m[newFloor][newRow][newCol].hasAgent == False:
    m[agentPos.floor][agentPos.row][agentPos.col].hasAgent = False
    m[newFloor][newRow][newCol].hasAgent = True
    return [True, Position3D(newFloor, newRow, newCol)]

  return [False, agentPos]