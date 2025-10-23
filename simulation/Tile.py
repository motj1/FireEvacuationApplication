class Tile:
  def __init__(self, kind='void', hp="0"):
    self.kind = kind
    self.hp = hp

  def isTraversable(self):
    if self.kind == "wall":
      return False
    else:
      return True
    
def createTile(c):
  t = Tile(parseKind(c), 10)
  return t

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
  elif c == 'P':
    return "prsn"
  else:  
    return "err"