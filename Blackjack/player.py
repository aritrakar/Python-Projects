import card


class Player:
    def __init__(self, cards):
        self.cards = cards

    def numCards(self):
        return len(self.cards)

    def getCard(self, index):
        return self.cards[index]

    def printCard(self, index):
        self.cards[index].printCard()

    def printAllCards(self):
        num = len(self.cards)  # self.numCards()
        for c in range(num):
            self.cards[c].printCard()

    def addCard(self, card):
        self.cards += [card]
        print("Added: ")
        card.printCard()

    def removeCard(self, index):
        return self.cards.pop(index)
