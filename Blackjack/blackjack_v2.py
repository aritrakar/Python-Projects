import card
from player import Player

# Initialize original cards array
cards = card.initializeCards()


# getCardSum(player) gets the total hand value of 'player'
def getCardSum(player):
    result = 0
    aces = 0
    for index in range(player.numCards()):
        c = player.getCard(index)
        if (c.getValue() == 1):
            aces += 1
        else:
            if c.getValue() >= 11 and c.getValue() <= 13:
                result += 10
            else:
                result += c.getValue()

    for _ in range(aces):
        if (result + 11 <= 21):
            result += 11
        elif (result + 1 <= 21):
            result += 1
    return result


# split(amount, playerAgent, dealerAgent) simulates "splitting" of a hand
def split(amount, playerAgent, dealerAgent):
    totalAmount = 0
    for roundNumber in range(0, 2):
        print("\nHAND {r}:".format(r=(roundNumber+1)))
        newPlayerAgent = Player([playerAgent.getCard(roundNumber),
                                 card.getRandomCard(cards)])
        print("Player cards:")
        newPlayerAgent.printAllCards()
        totalAmount += deal(amount, amount, newPlayerAgent)
    return totalAmount


# deal(amount, bet, playerAgent) plays a single round of 21
def deal(amount, bet, playerAgent):
    playerSum = getCardSum(playerAgent)

    dealerAgent = Player(
        [card.getRandomCard(cards), card.getRandomCard(cards)])
    dealerSum = getCardSum(dealerAgent)

    print("Player:")
    playerAgent.printAllCards()
    print("Dealer Card 1:")
    dealerAgent.printCard(0)

    # SPLITTING
    if playerAgent.getCard(0).getValue() == playerAgent.getCard(1).getValue():
        c = str(input("Do you want to split your cards? (Y/N)"))
        if c.lower() == 'y':
            print("\nSPLITTING CARDS!")
            result = split(amount, playerAgent, dealerAgent)
            amount *= 2
            return result
        else:
            print("Continuing without splitting...")

    # PLAYER
    choice = ''
    while (playerSum <= 21 or choice.lower() != 's'):
        if (playerSum == 21):
            print("Blackjack! You win this round!")
            amount += 1.5 * bet
            print("Amount: {a}".format(a=amount))
            return amount

        elif (playerSum > 21):
            print("You've bust. You LOSE! playerSum = {s}".format(s=playerSum))
            amount -= bet
            print("\nAmount: {a}".format(a=amount))
            return amount

        print("\nChoose:\n")
        choice = str(input("Hit (H) | Stand (S) | Double down (D): "))
        if (choice.lower() == 'h'):
            temp_card = card.getRandomCard(cards)
            playerAgent.addCard(temp_card)
            playerSum = getCardSum(playerAgent)
            print("Player:")
            playerAgent.printAllCards()
        elif (choice.lower() == 's'):
            break
        elif (choice.lower() == 'd'):
            bet *= 2
            temp_card = card.getRandomCard(cards)
            playerAgent.addCard(temp_card)
            playerSum = getCardSum(playerAgent)
            print("Doubled down! New bet amount: {b}".format(b=bet))

    # DEALER
    print("Dealer Card 2:")
    dealerAgent.printCard(1)
    if (dealerSum < 17):
        while(dealerSum <= 18):
            print("Dealer has hit!")
            # if (dealerSum < 21):
            temp_card = card.getRandomCard(cards)
            dealerAgent.addCard(temp_card)
            dealerSum = getCardSum(dealerAgent)
            print("dealerSum: {s}".format(s=dealerSum))
            print("Dealer cards:")
            dealerAgent.printAllCards()

    # FINAL OUTCOME
    print("Dealer sum: {d}".format(d=dealerSum))
    print("Player sum: {p}".format(p=playerSum))

    if(dealerSum == 21 and playerSum != 21):
        print("Dealer has Blackjack! You LOSE!")
        amount -= bet

    elif (dealerSum == playerSum):
        print("Pass")

    elif (dealerSum > 21):
        print("Dealer has bust. You win!")
        amount += bet

    elif (dealerSum < playerSum):
        print("Dealer has lower sum. You win!")
        amount += bet

    elif (dealerSum > playerSum):
        print("Dealer wins!")
        amount -= bet

    print("\nAmount: {a}".format(a=amount))
    return amount


# Main driver code
def main():
    rounds = 0
    amt = 0
    while True:
        rounds += 1
        print("\nROUND {r}:\n".format(r=rounds))
        if rounds == 1:
            toBet = int(input("How much would you like to bet? A: "))
            playerAgent = Player(
                [card.getRandomCard(cards), card.getRandomCard(cards)])
            amt += deal(amt, toBet, playerAgent)

        if rounds > 1:
            ch = str(input("Would you like to play again? (Y/N)"))
            if (ch.lower() == 'y'):
                toBet = int(input("How much would you like to bet? A: "))
                playerAgent = Player(
                    [card.getRandomCard(cards), card.getRandomCard(cards)])
                amt += deal(amt, toBet, playerAgent)
            else:
                print("You played {r} round(s). \nFinal amount: {a}".format(
                    r=(rounds-1), a=amt))
                break


if __name__ == '__main__':
    print("Welcome to Blackjack! Let's play...")
    main()
