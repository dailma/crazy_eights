from random import shuffle
from os import system

class Card(object):
	def __init__(self, suit, value, image=None):
		self.suit = suit
		self.value = value
		self.image = image

class Deck(object):
	def __init__(self):
		self.suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
		self.values = range(1, 14)
		self.deck = []
		self.buildDeck()
	def buildDeck(self):
		for suit in self.suits:
			for value in self.values:
				self.deck.append(Card(suit, value))
		self.shuffle()
		return self
	def shuffle(self):
		shuffle(self.deck)  # using shuffle from random
		return self
	def deal(self):
		if self.deck:  # not empty
			return self.deck.pop()  # removes and returns top card
		else:
			print "No more cards"
	def returnCard(self, card, reshuffle=False):
		self.deck.append(card)
		if reshuffle:
			self.shuffle()
		return self
	def reset(self):
		self.deck = []
		self.buildDeck()
		return self
class Player(object):
	def __init__(self):
		self.hand = []
	def showHand(self):
		pass
	def draw(self, card):
		if card:
			self.hand.append(card)
		return self
	def play(self, idx):
		return self.hand.pop(idx)

class Game(object):
	def __init__(self, numPlayers=4, handSize=8):
		self.numPlayers = numPlayers
		self.handSize =	handSize
		self.currentPlayer = 0  # could randomize
		self.deck = Deck()
		self.start()
	def start(self):
		self.players = []
		for i in range(self.numPlayers):
			self.players.append(Player())
		self.deck.reset()
		for i in range(self.handSize):
			for player in self.players:
				player.draw(self.deck.deal())
		self.discard = []
		self.discard.append(self.deck.deal())
		return self
	def nextPlayer(self):
		self.currentPlayer = (self.currentPlayer + 1)%self.numPlayers
		return self
	def handCounts(self):
		temp = []
		for player in self.players:
			temp.append(len(player.hand))
		return temp

theGame = Game()

# TODO: request user input for numPlayers and handSize

while True:
	system('cls')
	cPlayer = theGame.players[theGame.currentPlayer]
	print "\nCurrent player:", theGame.currentPlayer + 1
	for player, count in enumerate(theGame.handCounts()):
		print "Player", player + 1,"cards:", count
	print "Cards remaining: ", len(theGame.deck.deck)
	print "Current card: ", theGame.discard[-1].value, "of", theGame.discard[-1].suit
	print ""
	for idx, card in enumerate(cPlayer.hand):
		print idx,"-", card.value, "of", card.suit
	x = raw_input("Card # or D (for draw): ")
	if x.upper() == "Q":
		break
	elif x.upper() == "D":
		cPlayer.draw(theGame.deck.deal())
	elif int(x) >= 0 and int(x) < len(cPlayer.hand):
		if cPlayer.hand[int(x)].value == 8:
			print "0 - Hearts; 1 - Diamonds; 2 - Clubs; 3 - Spades"
			crazy = int(raw_input("Choose suit: "))
			cPlayer.hand[int(x)].suit = theGame.deck.suits[crazy]
		if cPlayer.hand[int(x)].value == 8 or theGame.discard[-1].value == cPlayer.hand[int(x)].value or theGame.discard[-1].suit == cPlayer.hand[int(x)].suit:
			temp = cPlayer.play(int(x))
			print "Card headed to discard:",temp.value,temp.suit
			theGame.discard.append(temp)
			theGame.nextPlayer()
		else:
			print "Invalid; try again"
