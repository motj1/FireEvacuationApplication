class Position:
  def __init__(self, row='0', col='0'):
    self.col = col
    self.row = row

  def __format__(self):
    return f"{self.col}, {self.row}"