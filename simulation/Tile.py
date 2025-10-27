# Tile object used to store map cell data
class Tile:
  def __init__(self, kind='void', hp="0", hasAgent=False):
    self.kind = kind
    self.hp = hp
    self.hasAgent = hasAgent

  def isTraversable(self):
    if self.kind == "wall":
      return False
    else:
      return True
    
# Helper function which handles tile creation
def createTile(c, hasAgent):
  t = Tile(parseKind(c), 10, hasAgent)

  # Add material dependent hp here

  return t

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
  # elif c == 'P':
  #   return "prsn"
  else:  
    return "err"