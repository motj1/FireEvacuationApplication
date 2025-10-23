from Position import Position

def bfsAgent(m, curr, w, h):
  q = []
  visited = [[False for _ in range(w)] for _ in range(h)]
  prev = [[[-1,-1] for _ in range(w)] for _ in range(h)]

  adjacencyCoords = [[0, 1], [1, 0], [0, -1], [-1, 0], [-1, -1], [1, 1], [-1, 1], [1, -1]]

  visited[curr.row][curr.col] = True
  q.append([curr.row, curr.col])

  while len(q) != 0:
    curr = q.pop(0)

    for i in range(len(adjacencyCoords)):
      newRow = curr[0] + adjacencyCoords[i][0]
      newCol = curr[1] + adjacencyCoords[i][1]

      if newRow >= h or newRow < 0 or newCol >= w or newCol < 0:
        continue

      if m[newRow][newCol].kind == "exit":
        prev[newRow][newCol] = curr
        return [prev, Position(newRow, newCol)]

      if visited[newRow][newCol] == False and m[newRow][newCol].isTraversable() == True:
        visited[newRow][newCol] = True
        prev[newRow][newCol] = curr
        q.append([newRow, newCol])

def drawPath(m, firstExit, prev):
  row = firstExit.row
  col = firstExit.col

  while prev[row][col][0] != -1:
    if m[row][col].kind != "exit":
      m[row][col].kind = "path"
    prevRow = row
    row = prev[prevRow][col][0]
    col = prev[prevRow][col][1]