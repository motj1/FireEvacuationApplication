from Position import *
# Tile object used to store map cell data
class Tile:
  def __init__(self, kind='void', hp="0", hasAgent=False):
    self.kind = kind
    self.hp = hp
    self.hasAgent = hasAgent

  def isTraversable(self):
    if self.kind in ["wall", "fire", "obst", "internal_wall"]:
      return False
    else:
      return True
    
  def getBurnProbability(self):
    if self.kind in ["void"] + [f"smoke{i}" for i in range(1,10)] + [f"smoke{c}" for c in ["A", "B", "C"]]:
      return 0.125
    elif self.kind in ["obst", "door"]:
      return 0.0625
    elif self.kind in ["strs", "internal_wall"]:
      return 0.03125
    else:
      return False

class Stairwell(Tile):
  def __init__(self, kind='void', hp="0", hasAgent=False, up=Position3D(-1,-1,-1), down=Position3D(-1,-1,-1)):
    super().__init__(kind, hp, hasAgent)
    self.up = up
    self.down = down

# Translate map characters into their 'kinds'
def parseKind(c):
  if c == '#':
    return "wall"
  elif c == '|':
    return "internal_wall"
  elif c == ' ':
    return "void"
  elif c == 'F':
    return "fire"
  elif c == 'O':
    return "obst"
  elif c == 'E':
    return "exit"
  elif c == 'S':
    return "strs"
  elif c == 'd':
    return "door"
  elif c == 'D':
    return 'frdr'
  elif c in ["i" for i in range(1,10)] or c in ['A', 'B', 'C']:
    return "smoke" + c
  else:  
    return "err"