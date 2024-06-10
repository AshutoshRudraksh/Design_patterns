class Square:
  def __init__(self, sideLength):
    self.sideLength = sideLength
  
  def getSideLength(self):
      return self.sideLength

class SquareHole:
  def __init__(self, sideLength):
    self.sideLength = sideLength
  
  def canFit(self, square):
    return self.sideLength >= square.getSideLength()

class Circle:
  def __init__(self, radius):
    self.radius = radius

  def getRadius(self):
    return self.radius

#adapter class
class CircleToSquareAdapter(Square):
  def __init__(self, circle):
    self.circle = circle

  def getSideLength(self):
    return 2*self.circle.getRadius()