import enum

class GridPosition(enum.Enum):
  EMPTY = 0
  YELLOW = 1
  RED = 2

class Grid:
  def __init__(self, rows, columns):
    self._rows = rows
    self._columns = columns
    self._grid = None
    self.initGrid()

  def initGrid(self):
    self._grid = [[GridPosition.EMPTY for _ in range(self._columns)] for _ in range(self._rows)]

  def getGrid(self):
    return self._grid

  def getColumnCount(self):
    return self._columns

  # drop the piece in the board
  def placePiece(self, column, piece):
    if column < 0 or colum >= self._columns:
      raise ValueError('Invalid column')
    if piece == GridPosition.EMPTY:
      raise ValueError('Invalid Piece')
    for row in range(self._rows-1,-1,-1):
      if self._grid[row][column] == GridPosition.EMPTY:
        self._grid[row][column] = piece
        return row

    # check if someone is winning
  def CheckWin(self, connectN, row, col, piece):
    count = 0
    # Check horizontal
    for c in range(self._columns):
      if self._grid[row][c] == piece:
        count+=1
      else: count =0
      if count == connectN: return True


    # check for vertical
    count = 0
    for r in range(self._rows):
      if self._grid[r][col] == piece:
        count +=1
      else: count =0
      if count == connectN:
        return True

    # check diagonal
    count = 0
    for r in range(self._rows):
      c = row + col - r
      if  c >=0 and c < self._columns and self._grid[r][c] == piece:
        count +=1
      else:
        count = 0
      if count == connectN:
        return True

    # check anti-diagonal
    count = 0
    for r in range(self._rows):
      c = col - row + r
      if c >= 0 and c< self._columns and self._grid[r][c] == piece:
        count +=1
      else:
        count = 0
      if count == connectN:
        return True

    return False


# player class
class Player:
  def __init__(self, name, pieceColor):
    self._name = name
    self._pieceColor = pieceColor

  def getName(self):
    return self._name

  def getPieceColor(self):
    return self._pieceColor

class Game:
  def __init__(self, grid, connectN, targetScore):
    self._grid = grid
    self._connectN = connectN
    self._targetScore = targetScore

    self._players = [
        Player('player 1', GridPosition.YELLOW),
        Player('player 2', GridPosition.RED)
    ]

    self._score = {}
    for player in self._players:
      self._score[player.getName()]=0

  def PrintBoard(self):
    print('Board:\n')
    grid = self._grid.getGrid()
    for i in range(len(grid)):
      row = ''
      for piece in grid[i]:
        if piece == GridPosition.EMPTY:
          row += '0 '
        elif piece == GridPosition.YELLOW:
          row += 'Y '
        elif piece == GridPosition.RED:
          row +='R '
      print(row)
    print('')

  def playMove(self, player):
    self.printBoard()
    print(f"{player.getName()}'s turn")
    colcnt = self.grid.getColumnCount()
    moveColumn = int(input(f"Enter column between {0} and {colcnt-1} to add piece: "))
    moveRow = self._grid.placePiece(moveColumn, player.getPieceColor())
    return (moveRow, moveColumn)

  def playRound(self):
    while True:
      for player in self._players:
        row, col = self.playMove(player)
        pieceColor = player.getPieceColor()
        if self._grid.checkWin(self._connectN, row, col, pieceColor):
          self._score[player.getName()] += 1
          return player

  def player(self):
    maxScore = 0
    winner = None
    while maxScore < self._targetScore:
      winner = self.playRound()
      print(f"{winner.getName()} won the round")
      maxScore = max(self._score[winner.getName()], maxScore)

      self._grid.initGrid() # reset the grid
    print(f"{winner.getName()} won the game")


grid = Grid(6,7)
game = Game(grid, 4, 2)
game.PrintBoard()

