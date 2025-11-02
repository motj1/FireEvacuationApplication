from Position import *
from Tile import *
from txtConverters import *

def bfs3D(m, curr, dims):
  if m[curr.floor][curr.row][curr.col].kind == "fire":
    return Position3D(-1, -1, -1)

  q = []
  visited = [[[False for _ in range(dims[i][1])] for _ in range(dims[i][0])] for i in range(len(dims))]
  prev = [[[Position3D(-1, -1, -1) for _ in range(dims[i][1])] for _ in range(dims[i][0])] for i in range(len(dims))]

  adjacencyCoords = [[0, 1], [1, 0], [0, -1], [-1, 0], [-1, -1], [1, 1], [-1, 1], [1, -1]]

  visited[curr.floor][curr.row][curr.col] = True
  q.append(curr)

  while len(q) != 0:
    curr = q.pop(0)

    if type(m[curr.floor][curr.row][curr.col]) is Stairwell:
      if (m[curr.floor][curr.row][curr.col].down.row >= 0):
        downCell = m[curr.floor][curr.row][curr.col].down
        if visited[downCell.floor][downCell.row][downCell.col] == True:
          continue
        visited[downCell.floor][downCell.row][downCell.col] = True
        prev[downCell.floor][downCell.row][downCell.col] = curr
        q.append(downCell)

    for i in range(len(adjacencyCoords)):
      newRow = curr.row + adjacencyCoords[i][0]
      newCol = curr.col + adjacencyCoords[i][1]

      if newRow >= dims[curr.floor][0] or newRow < 0 or newCol >= dims[curr.floor][1] or newCol < 0:
        continue

      if m[curr.floor][newRow][newCol].kind == "exit":
        prev[curr.floor][newRow][newCol] = curr

        return generateInstructionsBFS3D(prev, curr.floor, newRow, newCol)

      if visited[curr.floor][newRow][newCol] == False and m[curr.floor][newRow][newCol].isTraversable() == True:
        visited[curr.floor][newRow][newCol] = True
        prev[curr.floor][newRow][newCol] = curr
        q.append(Position3D(curr.floor, newRow, newCol))
  return Position3D(-1, -1, -1)

def generateInstructionsBFS3D(prev, floor, newRow, newCol):
  instructions = []
  row = newRow
  col = newCol

  while prev[floor][row][col].row != -1:
    instructions.insert(0, (Position3D(floor, row, col)))
    prevRow = row
    prevFloor = floor
    floor = prev[prevFloor][prevRow][col].floor
    row = prev[prevFloor][prevRow][col].row
    col = prev[prevFloor][prevRow][col].col
  return instructions[0]