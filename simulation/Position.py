class Position:
  def __init__(self, row='0', col='0'):
    self.col = col
    self.row = row

  def __format__(self):
    return f"{self.col}, {self.row}"
  
class Position3D:
  def __init__(self, floor='0', row='0', col='0'):
    self.floor = floor
    self.row = row
    self.col = col