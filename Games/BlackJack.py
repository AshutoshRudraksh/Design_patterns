from enum import Enum

class Suit(Enum):
  CLUBS, DIAMONDS, HEARTS, SPADES = 'clubs', 'diamonds', 'hearts', 'spades'

class Card:
  def __init__(self, suit, value):
    self._suit = suit
    self._value = value

  def getSuit(self):
    return self._suit

  def getValue(self):
    return self._value

  def print(self):
    print(self.getSuit(), self.getValue())

# hand will contain array of cards, and total score each time we add the card the score is recalculated

class Hand:
  def __init__(self):
    self._score = 0
    self._cards = []

  def addCard(self, card):
    self._cards.append(card)
    if card.getValue() == 1:
      self._score +=11 if self._score +11 <=21 else 1
    else:
      self._score += card.getValue()
    print(f"Score: {self._score}")

  def getScore(self):
    return self._score

  def getCards(self):
    return self._cards

  def print(self):
    for card in self.getCards():
      print(card.getSuit(), card.getValue())
      print(f"Score: {self._score}")





# Deck: It will have array of cards, and will b e responsible for shuffling and drawing cards
import random

class Deck:
  def __init__(self):
    self._cards = []
    for suit in Suit:
      for value in range(1,14):
        self._cards.append(Card(suit,min(value,10)))

  #print the deck
  def print(self):
    for card in self._cards:
      card.print()

  # shuffle the deck
  def shuffle(self):
    random.shuffle(self._cards)

  # draw random card
  def draw(self):
    return self._cards.pop()
  
# Player: Abstract class which has a Hand and can make move. THe Dealer and UserPlayer will extend this class to override makeMove()
from abc import ABC, abstractmethod

class Player(ABC):
  def __init__(self, hand):
    self._hand = hand

  def getHand(self):
    return self._hand

  def clearHand(self):
    self._hand = Hand()

  def addCard(self, card):
    self._hand.addCard(card)

  @abstractmethod
  def makeMove(self):
    pass
  

# UserPlayer having Balance and be able to place a bet.
# It will also override makemove() to prompt the user for input: returning "true" to draw a card and "false" to stop

class UserPlayer(Player):
  def __init__(self, balance, hand):
    super().__init__(hand)
    self._balance = balance

  def getBalance(self):
    return self._balance

  def placeBet(self, amount):
    if amount > self._balance:
      raise ValueError("Insufficient balance")
    self._balance -= amount
    return amount

  def reciveWinning(self, amount):
    self._balance += amount

  def makeMove(self):
    if self.getHand().getScore() > 21:
      return False
    move = input(f"Do you want to draw a card? (y/n): ")
    return move == "y"
# Dealer need not place a bet or recieve winning. It will override makeMove() but they will draw until hand value>=targetSCore
#
class Dealer(Player):
  def __init__(self, hand):
    super().__init__(hand)
    self._targetScore = 17

  def updateTargetScore(self, score):
    self._targetScore = score

  def makeMove(self):
    return self.getHand().getScore() < self._targetScore
  

# Game Round the game control
class GameRound:
  def __init__(self, player , dealer, deck ):
    self._player = player
    self._dealer = dealer
    self._deck = deck

  def getBetUser(self):
    amount = int(input("Enter bet amount: "))
    return amount

  def dealInitialCards(self):
    for i in range(2):
      self._player.addCard(self._deck.draw())
      self._dealer.addCard(self._deck.draw())
    print("Player's hand:")
    self._player.getHand().print()
    dealerCard = self._dealer.getHand().getCards()[0]
    print("Dealer's hand:")
    dealerCard.print()

  def cleanupRound(self):
    self._player.clearHand()
    self._dealer.clearHand()
    print('Player balance: ', self._player.getBalance())

  def play(self):
    self._deck.shuffle()

    if self._player.getBalance() <= 0:
      print("You're out of money!")
      return
    userBet = self.getBetUser()
    self._player.placeBet(userBet)
    self.dealInitialCards()

    # user make move
    while self._player.makeMove():
      drawnCard = self._deck.draw()
      print('Player draws a card:', drawnCard.getSuit(), drawnCard.getValue())
      self._player.addCard(drawnCard)
      print('Player hand:', self._player.getHand().getScore())

    if self._player.getHand().getScore() > 21:
      print("You busted!")
      self.cleanupRound()
      return

    # dealer make move
    while self._dealer.makeMove():
      self._dealer.addCard(self._deck.draw())


    # determine winner
    if self._dealer.getHand().getScore() > 21 or self._player.getHand().getScore() > self._dealer.getHand().getScore():
      print("Player wins!")
      self._player.reciveWinning(userBet*2)
    elif self._dealer.getHand().getScore() > self._player.getHand().getScore():
      print('Player loses!')
    else:
      print("Game end in a draw!")
      self._player.reciveWinning(userBet)
    self.cleanupRound()
    
# we run the game until the player runs out of money
player = UserPlayer(100, Hand())
dealer = Dealer(Hand())

while player.getBalance() > 0:
  gameRound = GameRound(player, dealer, Deck()).play()
