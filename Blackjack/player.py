import card

class Player:
    def __init__(self, cards):
        self.cards = cards

    # numCards() returns the number of cards in the Player's hand
    def numCards(self):
        return len(self.cards)

    # getCard(index) returns the card at index 'index' of the player's hand
    def getCard(self, index):
        return self.cards[index]

    # printCard(index) prints the card at index 'index' of the player's hand
    def printCard(self, index):
        self.cards[index].printCard()

    # printAllCards() prints all the cards in player's hand
    def printAllCards(self):
        num = len(self.cards)
        for c in range(num):
            self.cards[c].printCard()

    # addCard(card) adds Card 'card' to player's hand
    def addCard(self, card):
        self.cards += [card]
        print("Added: ")
        card.printCard()

    # removeCard(index) removes Card at 'index' from player's hand
    def removeCard(self, index):
        return self.cards.pop(index)
