import random

"""
Legend:
Suits: 0: Clubs; 1: Diamonds; 2: Hearts; 3: Spades
Denominations:
1: Ace
2 - 10: Number cards
11: Jack
12: Queen
13: King
"""

clubsUnicode = '\U00002663'
diamondUnicode = '\U00002666'
heartsUnicode = '\U00002665'
spadeUnicode = '\U00002660'
unicodes = [clubsUnicode, diamondUnicode, heartsUnicode, spadeUnicode]


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def getSuit(self):
        return self.suit

    def getValue(self):
        return self.value

    def printCard(self):
        print(unicodes[self.getSuit()], self.getValue())


# initializeCards() initializes all the cards in the deck and returns an
# array containing all 52 cards.
def initializeCards():
    cards = []
    for suit in range(0, 4):
        for denom in range(1, 14):
            cards.append(Card(suit, denom))
    return cards


# getRandomCard(cards) returns a random card from array of Cards 'cards'
def getRandomCard(cards):
    return cards.pop(random.randint(0, len(cards) - 1))
