import random

clubs = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC', 'AC']
spades = ['2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS', 'AS']
hearts = ['2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH', 'AH']
diamonds = ['2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD', 'AD']

cards = clubs + spades + hearts + diamonds 

def getRandomCard():
    randomIndex = random.randint(0,len(cards)-1)
    randomCard = cards.pop(randomIndex)
    return randomCard

def getCardValue(card):
    prefix = card[:-1]
    if prefix in ['J','Q','K']:
        return 10
    elif prefix == 'A':
        return 'A'
    else:
        return int(prefix)

def getCardSum(cardsList):
    result = 0
    aces = 0
    for card in cardsList:
        if card[:-1] == 'A':
            aces += 1
        elif card[:-1] in ['J','Q','K']:
            result += 10
        else:
            temp = getCardValue(card)
            result += temp
            
    for x in range(aces):
        if (result + 11 <= 21):
            result += 11
        elif (result + 1 <= 21):
            result += 1
    return result
        
def deal(amount, bet):
    playerCard1 = getRandomCard()
    playerCard2 = getRandomCard()  
    playerCards = [playerCard1, playerCard2] 
    playerSum = getCardSum(playerCards)
    
    dealerCard1 = getRandomCard()
    dealerCard2 = getRandomCard()
    dealerCards = [dealerCard1, dealerCard2] 
    dealerSum = getCardSum(dealerCards)

    #PLAYER PART
    print("Player cards: {c1}, {c2}".format(c1=playerCard1, c2=playerCard2))
    print("Dealer card 1: {d1}".format(d1=dealerCard1))

    while (playerSum <= 21 or choice.lower() != 's'):
        if (playerSum == 21):
            print("Blackjack! You win this round!")
            amount += 1.5*bet
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
            temp_card = getRandomCard()
            playerCards += [temp_card]
            playerSum = getCardSum(playerCards)
            print("Your new card: {c}".format(c=temp_card))
            print("playerCards: ", playerCards)         
        elif (choice.lower() == 's'):
            break
        elif (choice.lower() == 'd'):
            bet *= 2
            temp_card = getRandomCard()
            playerCards += [temp_card]
            playerSum = getCardSum(playerCards)

    #DEALER PART   
    print("Dealer card 2: {d2}".format(d2=dealerCard2))
    if (dealerSum < 17):
        while(dealerSum <= 18):
            print("Dealer has hit!")
            #if (dealerSum < 21):
            temp_card = getRandomCard()
            dealerCards += [temp_card]
            dealerSum = getCardSum(dealerCards)
            print("dealerSum: {s}".format(s=dealerSum))
            print("Dealer cards: {ds}".format(ds=dealerCards))

    #FINAL OUTCOME
    print("Dealer sum: {d}".format(d=dealerSum))
    print("Player sum: {p}".format(p=playerSum))
    
    if(dealerSum == 21 and playerSum != 21):
        print("Dealer has Blackjack! You LOSE! \n dealerSum = {s}".format(s=dealerSum))
        amount -= bet

    elif (dealerSum == playerSum or (dealerSum == 21 and playerSum == 21)):
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
    
def main():
    rounds = 0
    amt = 0
    while True:
        rounds += 1
        print("\nROUND {r}:\n".format(r=rounds))
        if rounds == 1:
            toBet = int(input("How much would you like to bet? A: "))
            amt += deal(amt, toBet)
            
        if rounds > 1:
            ch = str(input("Would you like to play again? (Y/N)"))
            if (ch.lower() == 'y'):
                toBet = int(input("How much would you like to bet? A: "))
                amt += deal(amt, toBet)                
            else:
                print("You played {r} round(s). \nFinal amount: {a}".format(r=(rounds-1), a=amt))
                break
    
if __name__ == '__main__':
    print("Welcome to Blackjack! Let's play...")
    main()
