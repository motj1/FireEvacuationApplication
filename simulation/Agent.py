from Position import *

# Move a person to a given position if the position is valid to move to
def moveAgent(m, agentPos, agentInstructions):
  newRow = agentInstructions.row
  newCol = agentInstructions.col
  if abs(agentPos.col - newCol) <= 1 and abs(agentPos.row - newRow) <= 1 and m[newRow][newCol].isTraversable() and m[newRow][newCol].hasAgent == False:
    m[agentPos.row][agentPos.col].hasAgent = False
    m[newRow][newCol].hasAgent = True
    return [True, Position(newRow, newCol)]
  else:
    return [False, agentPos]