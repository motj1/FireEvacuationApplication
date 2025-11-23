from algorithm import *
from Position import *
from txtConverters import *
from Agent import *
from txtConverters import *
import random
from fire import *

def spreadSmoke(m, dims):
  for i in range(len(dims)):
    for j in range(dims[i][0]):
      for k in range(dims[i][1]):
        curTile = m[i][j][k]
        if curTile.kind == "fire":
          spreadSmokeIntensity(m, i, j, k)

  for intensity in range(1, 10):
      for i in range(len(dims)):
        for j in range(dims[i][0]):
          for k in range(dims[i][1]):
            curTile = m[i][j][k]
            if curTile.kind == f"smoke{intensity}":
              spreadSmokeIntensity(m, i, j, k)

  for intensity in ["A", "B", "C"]:
      for i in range(len(dims)):
        for j in range(dims[i][0]):
          for k in range(dims[i][1]):
            curTile = m[i][j][k]
            if curTile.kind == f"smoke{intensity}":
              spreadSmokeIntensity(m, i, j, k)

      
        
def spreadSmokeIntensity (m, i, j, k):
  curTile = m[i][j][k]

  smokeSpreadTiles = []
  adjacencyCoords = [[0, 1], [1, 0], [0, -1], [-1, 0], [-1, -1], [1, 1], [-1, 1], [1, -1]]

  for coord in adjacencyCoords:
    row = j + coord[0]
    col = k + coord[1]
    destTile = m[i][row][col]

    if canSmokeSpread(curTile, destTile):
      smokeSpreadTiles.append((destTile, getGradientSmoke(curTile)))

  if type(curTile) is Stairwell:
    if (curTile.down.row >= 0):
      d = curTile.down
      downCell = m[d.floor][d.row][d.col]
      if canSmokeSpread(curTile, downCell):
        smokeSpreadTiles.append((downCell, getGradientSmoke(curTile)))
    if (curTile.up.row >= 0):
      u = curTile.up
      upCell = m[u.floor][u.row][u.col]
      if canSmokeSpread(curTile, upCell):
        smokeSpreadTiles.append((upCell, getGradientSmoke(curTile)))

  for tile, newKind in smokeSpreadTiles: 
    if tile.kind[0:5] == "smoke" and tile.kind[5] < newKind[5]:
      continue
    tile.kind = newKind


# smoke can spread off fire and smoke tiles, but cannot spread to fire
def canSmokeSpread (sourceTile: Tile, destTile: Tile) -> bool:
  if destTile.kind in ["fire", "exit"] or not destTile.isTraversable():
    return False

  # if destTile isn't fire and sourceTile is fire, then smoke can always spread
  if sourceTile.kind == "fire":
    return True
  elif sourceTile.kind[0:5] == "smoke":
    charMap = {"A":10, "B":11, "C":12, "D":13}
    sourceInty = int(sourceTile.kind[5]) if sourceTile.kind[5].isdigit() else charMap[sourceTile.kind[5]]

    if not smokeSpreadHappens(sourceInty):
      return False
    
    if destTile.kind[0:5] == "smoke":
      destInty = int(destTile.kind[5]) if destTile.kind[5].isdigit() else charMap[destTile.kind[5]]
      return sourceInty > destInty
    else:
      return True
  else:
    return False
  
def getGradientSmoke(sourceTile: Tile) -> str:
  intMap = {9: "9", 10:"A", 11:"B", 12:"C", 13:"D"}
  charMap = {"9": 9, "A":10, "B":11, "C":12, "D":13}

  if sourceTile.kind == "fire":
    return "smoke1"
  elif sourceTile.kind[5].isdigit() and int(sourceTile.kind[5]) < 9:
    return "smoke" + str(int(sourceTile.kind[5])+1)
  else:
    return "smoke" + intMap[charMap[sourceTile.kind[5]]+1]

def smokeSpreadHappens (sourceIntensity: int) -> bool:
  # smoke chance is proportional to intensity
  return random.randint(1, 2*(sourceIntensity+1)) <= 1