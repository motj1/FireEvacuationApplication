from Position import *
# Tile object used to store map cell data
class Tile:
  def __init__(self, kind='void', hp="0", hasAgent=False):
    self.kind = kind
    self.hp = hp
    self.hasAgent = hasAgent

  def isTraversable(self):
    if self.kind == "wall" or self.kind == "fire" or self.kind == "obst":
      return False
    else:
      return True
    
  def isBurnable(self):
    if self.kind in ["void", "obst", "strs"]:
      return True
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
  elif c == 'D':
    return "door"
  else:  
    return "err"