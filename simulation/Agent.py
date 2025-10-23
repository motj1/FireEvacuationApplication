import Position

def moveAgent(m, agentPos, newCol, newRow):
  if abs(agentPos.col - newCol) <= 1 and abs(agentPos.row - newRow) <= 1 and m[newRow][newCol].isTraversable():
    m[agentPos.row][agentPos.col].kind = "void"
    m[newRow][newCol].kind = "prsn"
    return Position(newRow, newCol)
  else:
    return agentPos