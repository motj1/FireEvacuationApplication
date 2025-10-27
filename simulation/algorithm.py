from Position import Position

# Runs a BFS originating from the given person until an exit tile is found
# Must return an ordered list of instructions determined by the algorithm
def bfs(m, curr, w, h):
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
        return generateInstructionsBFS(prev, newRow, newCol)

      if visited[newRow][newCol] == False and m[newRow][newCol].isTraversable() == True:
        visited[newRow][newCol] = True
        prev[newRow][newCol] = curr
        q.append([newRow, newCol])

# Generates an ordered list of coordinates the agent needs to move through to reach its nearest exit 
def generateInstructionsBFS(prev, newRow, newCol):
  instructions = []
  row = newRow
  col = newCol

  while prev[row][col][0] != -1:
    instructions.insert(0, (Position(row, col)))
    prevRow = row
    row = prev[prevRow][col][0]
    col = prev[prevRow][col][1]

  return instructions