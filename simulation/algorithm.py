from Position import *
from Tile import *
from txtConverters import *
import math
import heapq

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
        
        if visited[downCell.floor][downCell.row][downCell.col] != True:
          visited[downCell.floor][downCell.row][downCell.col] = True
          prev[downCell.floor][downCell.row][downCell.col] = curr
          q.append(downCell)

      if (m[curr.floor][curr.row][curr.col].up.row >= 0):
        upCell = m[curr.floor][curr.row][curr.col].up

        if visited[upCell.floor][upCell.row][upCell.col] != True:
          visited[upCell.floor][upCell.row][upCell.col] = True
          prev[upCell.floor][upCell.row][upCell.col] = curr
          q.append(upCell)

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

class Cell:
    def __init__(self):
        # Parent cell's row index
        self.parent_i = -1
        # Parent cell's column index
        self.parent_j = -1
        # Parent cell's floor index
        self.parent_k = -1
        # Total cost of the cell (g + h)
        self.f = float('inf')
        # Cost from start to this cell
        self.g = float('inf')
        # Heuristic cost from this cell to destination
        self.h = 0

def is_valid(floor, row, col, dims):
    return (floor >= 0) and (floor < len(dims)) and (row >= 0) and (row < dims[floor][0]) and (col >= 0) and (col < dims[floor][1])

def calculate_h_value_single(src, dest):
    return ((src.row - dest.row) ** 2 + (src.col - dest.col) ** 2) ** 0.5 + (src.floor - dest.floor) if (src.floor - dest.floor) >= 0 else (dest.floor - src.floor)

def calculate_h_value(src, dests):
    return min([calculate_h_value_single(src, dest) for dest in dests])

def generatePathAStar3D(cell_details, dest):
    instructions = []
    floor = dest.floor
    row = dest.row
    col = dest.col

    while cell_details[floor][row][col].parent_i != row or cell_details[floor][row][col].parent_j != col or cell_details[floor][row][col].parent_k != floor:
        instructions.append(Position3D(floor, row, col))
        prevRow = row
        prevFloor = floor
        floor = cell_details[floor][row][col].parent_k
        row = cell_details[prevFloor][row][col].parent_i
        col = cell_details[prevFloor][prevRow][col].parent_j
    
    if (len(instructions) == 0):
        print("Screams ...")
        return Position3D(-1, -1, -1)
    return instructions[-1]

def astar(map, src, dims):
    if map[src.floor][src.row][src.col].kind == "fire":
        return Position3D(-1, -1, -1)

    dests = []
    foundExit = False

    for i in range(dims[src.floor][0]):
        for j in range(dims[src.floor][1]):
            if (type(map[src.floor][i][j]) is Stairwell and not foundExit) or ((map[src.floor][i][j]).kind == "exit" and foundExit):
                dests.append(Position3D(src.floor, i, j))
            elif ((map[src.floor][i][j]).kind == "exit"):
                dests = [Position3D(src.floor, i, j)]
                foundExit = True

    closed_list = [[[False for _ in range(dims[i][1])] for _ in range(dims[i][0])] for i in range(len(dims))]
    cell_details = [[[Cell() for _ in range(dims[i][1])] for _ in range(dims[i][0])] for i in range(len(dims))]

    adjacencyCoords = [[0, 1], [1, 0], [0, -1], [-1, 0], [-1, -1], [1, 1], [-1, 1], [1, -1]]

    i = src.row
    j = src.col
    k = src.floor
    cell_details[k][i][j].f = 0
    cell_details[k][i][j].g = 0
    cell_details[k][i][j].h = 0
    cell_details[k][i][j].parent_k = k
    cell_details[k][i][j].parent_i = i
    cell_details[k][i][j].parent_j = j

    open_list = []
    heapq.heappush(open_list, (0.0, k, i, j))

    found_dest = False

    while len(open_list) > 0:
        p = heapq.heappop(open_list)

        k = p[1]
        i = p[2]
        j = p[3]
        closed_list[k][i][j] = True

        # Handle stairwell
        if type(map[k][i][j]) is Stairwell:
            new_k = map[k][i][j].down.floor # can make going up but cant be bothered for now (would be the same as with other directions)
            new_i = map[k][i][j].down.row
            new_j = map[k][i][j].down.col
            if is_valid(new_k, new_i, new_j, dims) and map[new_k][new_i][new_j].isTraversable() and not closed_list[new_k][new_i][new_j]:
                if map[new_k][new_i][new_j].kind == "exit":
                    cell_details[new_k][new_i][new_j].parent_i = i
                    cell_details[new_k][new_i][new_j].parent_j = j
                    cell_details[new_k][new_i][new_j].parent_k = k
                    found_dest = True
                    return generatePathAStar3D(cell_details, Position3D(new_k, new_i, new_j))# gen path
                else:
                    # Calculate the new f, g, and h values
                    g_new = cell_details[k][i][j].g + 1.0
                    h_new = calculate_h_value(Position3D(new_k, new_i, new_j), dests)
                    f_new = g_new + h_new

                    if cell_details[new_k][new_i][new_j].f == float('inf') or cell_details[new_k][new_i][new_j].f > f_new:
                        # Add the cell to the open list
                        heapq.heappush(open_list, (f_new, new_k, new_i, new_j))
                        # Update the cell details
                        cell_details[new_k][new_i][new_j].f = f_new
                        cell_details[new_k][new_i][new_j].g = g_new
                        cell_details[new_k][new_i][new_j].h = h_new
                        cell_details[new_k][new_i][new_j].parent_k = k
                        cell_details[new_k][new_i][new_j].parent_i = i
                        cell_details[new_k][new_i][new_j].parent_j = j
        else:
            for dir in adjacencyCoords:
                new_i = i + dir[0]
                new_j = j + dir[1]
                if is_valid(k, new_i, new_j, dims) and map[k][new_i][new_j].isTraversable() and not closed_list[k][new_i][new_j]:
                    if map[k][new_i][new_j].kind == "exit":
                        cell_details[k][new_i][new_j].parent_i = i
                        cell_details[k][new_i][new_j].parent_j = j
                        cell_details[k][new_i][new_j].parent_k = k
                        found_dest = True
                        return generatePathAStar3D(cell_details, Position3D(k, new_i, new_j))# gen path
                    else:
                        # Calculate the new f, g, and h values
                        g_new = cell_details[k][i][j].g + 1.0
                        h_new = calculate_h_value(Position3D(k, new_i, new_j), dests)
                        f_new = g_new + h_new

                        if cell_details[k][new_i][new_j].f == float('inf') or cell_details[k][new_i][new_j].f > f_new:
                            # Add the cell to the open list
                            heapq.heappush(open_list, (f_new, k, new_i, new_j))
                            # Update the cell details
                            cell_details[k][new_i][new_j].f = f_new
                            cell_details[k][new_i][new_j].g = g_new
                            cell_details[k][new_i][new_j].h = h_new
                            cell_details[k][new_i][new_j].parent_k = k
                            cell_details[k][new_i][new_j].parent_i = i
                            cell_details[k][new_i][new_j].parent_j = j


    return Position3D(-1, -1, -1)