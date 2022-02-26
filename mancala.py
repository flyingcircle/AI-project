import numpy as np

class TurnEndAction:
  TURN_END = 0
  GO_AGAIN = 1
  CAPTURE_PIT = 2

class MancalaBoard:

  P1_STORE = 6
  P2_STORE = 13

  def __init__(self) -> None:
    self.board = np.array([4,4,4,4,4,4,0,4,4,4,4,4,4,0])

  # returns true Go again
  def playPit(self, i) -> TurnEndAction:
    assert i != self.P1_STORE and i != self.P2_STORE
    isPlayer1Move = i < 6
    inHand = self.board[i]
    self.board[i] = 0
    while(inHand != 0):
      # skip the opponent's store
      if i == self.P2_STORE or (i == self.P2_STORE - 1 and isPlayer1Move):
        i = 0
      elif i == self.P1_STORE - 1 and not isPlayer1Move:
        i += 2
      else:
        i += 1
      self.board[i] += 1
      inHand -= 1
    # go again if last move is in player's store.
    if (isPlayer1Move and i == self.P1_STORE) or (not isPlayer1Move and i == self.P2_STORE):
      return True
    # capture pit if last move is in player's own empty pit.
    elif ((isPlayer1Move and i < 6) or (not isPlayer1Move and i > 6)) and self.board[i] == 1:
      self.capturePit(i)
    return False

  def capturePit(self, i):
    if i < self.P1_STORE:
      self.board[self.P1_STORE] += self.board[i]
      self.board[self.P1_STORE] += self.board[12 - i]
    else:
      self.board[self.P2_STORE] += self.board[i]
      self.board[self.P2_STORE] += self.board[12 - i]
    self.board[i] = 0
    self.board[12 - i] = 0

  # at the end of the game you collect the remaining stones into the store.
  def collectRemaining(self):
    self.board[self.P1_STORE] += sum(self.board[0:6])
    self.board[self.P2_STORE] += sum(self.board[7:13])

  def isGameOver(self):
    return sum(self.board[0:6]) == 0 or sum(self.board[7:13]) == 0

  def isPlayer1Winning(self):
    return self.board[self.P1_STORE] > self.board[self.P2_STORE]

  def isGameTie(self):
    return self.board[self.P1_STORE] == self.board[self.P2_STORE]


class Player:

  def __init__(self, isPlayer1) -> None:
    self.isPlayer1 = isPlayer1

  def getNextMove(self, boardState: np.array) -> int:
    pass


class MancalaGame:

  def __init__(self, player1: Player, player2: Player) -> None:
    self.board = MancalaBoard()
    self.player1 = player1
    self.player2 = player2
    self.isPlayer1Turn = True

  # returns 1 if Player 1 won
  def run(self):
    while(not self.board.isGameOver()):
      currPlayer = self.player1 if self.isPlayer1Turn else self.player2
      nextMove = currPlayer.getNextMove(self.board.board)
      if not self.board.playPit(nextMove):
        self.isPlayer1Turn = not self.isPlayer1Turn
    self.board.collectRemaining()
    if self.board.isPlayer1Winning():
      return 1
    elif self.board.isGameTie():
      return 0
    else:
      return -1



