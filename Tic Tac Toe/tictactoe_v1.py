'''
For different modes use the following combinations of functions (change in main()):
1. Computer (Smart) vs Human: bestMove2(board, depth1) and nextTurnHuman(board)
2. Computer (Random) vs Human: nextTurnRandom(board) and nextTurnHuman(board) 
3. Computer vs Computer: bestMove(board, depth1) or bestMove2(board, depth1) with aiAgent2(board, depth2)
'''
import math, random

initial_board = [['','',''],['','',''], ['','','']]
ai = 'X'
human = 'O'
scores = {'X': 1, 'O':-1, 'tie': 0, '': 0}

def clearBoard():
    return [['','',''],['','',''], ['','','']]

def printBoard(board):
    for i in range(0,3):
        print(list(map(lambda x: x, board[i]))) #"".join(x) useless
    print("\n")

def updateBoard(board, move, player):
    prev = board[move[0]][move[1]]
    if (board[move[0]][move[1]] == ''):
        board[move[0]][move[1]] = player
        #printBoard(board)
        #return board
    else:
        board[move[0]][move[1]] = prev
        print("INVALID MOVE")
        print("\n")
    
def checkWinner(board):
    winner = ''
    winningPath = ''
    openSpots = 0

    for i in range(0,3): #Horizontal
        if (board [i][0] == board[i][1] == board[i][2] != ''):
            winner = board[i][0]
            winningPath = "Horizontal {n}".format(n=i)
            break

    for i in range(0,3): #Vertical
        if (board [0][i] == board[1][i] == board[2][i] != ''):
            winner = board[0][i]
            winningPath = "Vertical {n}".format(n=i)
            break
            
    #Diagonals:
    if (board[0][0] == board[1][1] == board[2][2] != ''):
        winner = board[0][0]
        winningPath = "Diagonal: Left to Right"
    elif (board[0][2] == board[1][1] == board[2][0] != ''):
        winner = board[0][2]
        winningPath = "Diagonal: Right to Left"
        
    #Open spots
    for i in range(0,3):
        for j in range(0,3):
            if (board[i][j] == ''):
                openSpots += 1
                
    if (winner == '' and openSpots == 0):
        return 'tie'
    else:
        #print(winningPath)
        #print("{s} wins!".format(s=winner))
        return winner

def nextTurnRandom(board):
    available = []
    for i in range(0,3):
        for j in range(0,3):
            if (board[i][j] == ''):
                available.append((i,j))
    #print("available: ", available)
    randomMove = random.choice(available)
    print("randomMove: ", randomMove)
    return updateBoard(board, randomMove, ai)   

def nextTurnHuman(board):
    humanMove = tuple(map(int, input("Your move: ").split(" ")))
    res = updateBoard(board, humanMove, human)
    if (res == "INVALID MOVE"):
        nextTurnHuman(board)
    else:
        return res

#Minimax algorithm
def minimax(board, depth, isMaximizing):
    result = checkWinner(board)
    if (result != '' or depth == 0):
        #print("result inside minimax: ", result)
        return scores[result]

    if (isMaximizing):
        bestScore = -math.inf
        for i in range(0,3):
            for j in range(0,3):
                if (board[i][j] == ''):
                    board[i][j] = ai
                    score = minimax(board, depth-1, False)
                    board[i][j] = ''
                    bestScore = max(score, bestScore)
        return bestScore
    else:
        bestScore = math.inf
        for i in range(0,3):
            for j in range(0,3):
                if (board[i][j] == ''):
                    board[i][j] = human
                    score = minimax(board, depth-1, True)
                    board[i][j] = ''
                    bestScore = min(score, bestScore)
        return bestScore

#Minimax algorithm with alpha-beta pruning
def minimaxWithPruning(board, depth, alpha, beta, isMaximizing):
    result = checkWinner(board)
    if (result != '' or depth == 0):
        #print("result inside minimax: ", result)
        return scores[result]

    if (isMaximizing):
        maxScore = -math.inf
        for i in range(0,3):
            for j in range(0,3):
                if (board[i][j] == ''):
                    board[i][j] = ai
                    score = minimaxWithPruning(board, depth-1, alpha, beta, False)
                    board[i][j] = ''
                    maxScore = max(score, maxScore)
                    alpha = max(alpha, score)
                if beta <= alpha:
                    break
        return maxScore
    else:
        minScore = math.inf
        for i in range(0,3):
            for j in range(0,3):
                if (board[i][j] == ''):
                    board[i][j] = human
                    score = minimaxWithPruning(board, depth-1, alpha, beta, True)
                    board[i][j] = ''
                    minScore = min(score, minScore)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return minScore
    
def bestMove(board, depth):
    #AI to make its turn
    score = 0
    bestScore = -math.inf
    move = (-1, -1)
    for i in range(0,3):
        for j in range(0,3):
            if (board[i][j] == ''):
                board[i][j] = ai
                score = minimax(board, depth, False)
                board[i][j] = ''
                if(score > bestScore):
                    bestScore = score
                    move = (i, j)
    print("Comptuer's move: {m}".format(m=move))
    updateBoard(board, move, ai)

#bestMove with pruning
def bestMove2(board, depth):
    #AI to make its turn
    score = 0
    bestScore = -math.inf
    move = (-1, -1)
    alpha = -math.inf
    beta = math.inf
    for i in range(0,3):
        for j in range(0,3):
            if (board[i][j] == ''):
                board[i][j] = ai
                score = minimaxWithPruning(board, depth, alpha, beta, False)
                board[i][j] = ''
                if(score > bestScore):
                    bestScore = score
                    move = (i, j)
    print("Comptuer's move: {m}".format(m=move))
    updateBoard(board, move, ai)

def aiAgent2(board, depth):
    #AI to make its turn
    score = 0
    bestScore = -math.inf
    move = (-1, -1)
    for i in range(0,3):
        for j in range(0,3):
            if (board[i][j] == ''):
                board[i][j] = human
                score = minimax(board, depth, True)
                board[i][j] = ''
                if(score > bestScore):
                    bestScore = score
                    move = (i, j)
    print("Comptuer's move: {m}".format(m=move))
    updateBoard(board, move, human)
    
def main():
    board = initial_board
    turn = random.randint(0,1)
    print("turn: ", turn)
    result = ''
    printBoard(board)
    depth1 = 0
    depth2 = 0
    while (result == ''):
        if (turn == 0):
            bestMove2(board, depth1)
            #bestMove(board, depth1)
            #nextTurnRandom(board)
            turn = turn^1
            depth1 += 1
        else:
            nextTurnHuman(board)
            #aiAgent2(board, depth2)
            depth2 += 1
            turn = turn^1
        result = checkWinner(board)
        printBoard(board)
    if(result == 'tie'):
        print("Tie!")
    else:
        print("{r} wins!".format(r=result))

if __name__ == "__main__":
    print("Starting game...\n")
    main()

'''Interesting future possibilities:
1. Larger boadr
2. More players?
3. Other game (like connect 4)
4. Animation and timing
5. 3D tic tac toe
'''
