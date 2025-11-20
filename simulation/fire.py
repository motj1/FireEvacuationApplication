from Tile import *
import random

def spreadFire(m, dims, pessimism):
  tilesSpreadTo = []

  for i in range(len(dims)):
    for j in range(dims[i][0]):
      for k in range(dims[i][1]):
        if m[i][j][k].kind == "fire":
          adjacencyCoords = [[0, 1], [1, 0], [0, -1], [-1, 0], [-1, -1], [1, 1], [-1, 1], [1, -1]]

          for coord in adjacencyCoords:
            row = j + coord[0]
            col = k + coord[1]

            probability = m[i][row][col].getBurnProbability() * pessimism
            if spreadHappens(probability):
              tilesSpreadTo.append(m[i][row][col])

          if type(m[i][j][k]) is Stairwell:
            if (m[i][j][k].down.row >= 0):
              d = m[i][j][k].down
              downCell = m[d.floor][d.row][d.col]
              probability = downCell.getBurnProbability() * pessimism
              if spreadHappens(probability):
                tilesSpreadTo.append(m[d.floor][d.row][d.col])
            if (m[i][j][k].up.row >= 0):
              u = m[i][j][k].up
              upCell = m[u.floor][u.row][u.col]
              probability = upCell.getBurnProbability() * pessimism
              if spreadHappens(probability):
                tilesSpreadTo.append(m[u.floor][u.row][u.col])

  for tile in tilesSpreadTo:
    tile.kind = "fire"

def spreadHappens(probability):
  return random.random() >= (1 - probability)