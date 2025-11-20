def spreadSmoke(m, dims):
  smokeSpreadTiles = []

  for i in range(len(dims)):
    for j in range(dims[i][0]):
      for k in range(dims[i][1]):
        curTile = m[i][j][k]
        # iterate through fire and smoke1-4 nodes to spread smoke as smoke1-5
        if curTile.kind in ["fire"] + [f"smoke{i}" for i in range(1,6)]:
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
    if not smokeSpreadHappens(int(sourceTile.kind[5])):
      return False
    if destTile.kind[0:5] == "smoke":
      return int(sourceTile.kind[5]) > int(destTile.kind[5])
    else:
      return True
  else:
    return False
  
def getGradientSmoke(sourceTile: Tile) -> str:
  if sourceTile.kind == "fire":
    return "smoke1"
  else:
    return "smoke" + str(int(sourceTile.kind[5])+1)

def smokeSpreadHappens (sourceIntensity: int) -> bool:
  # smoke chance is proportional to intensity
  return random.randint(1, (sourceIntensity+2)//3) <= 1