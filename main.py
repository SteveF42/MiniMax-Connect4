# first make connect 4
# make the mini max algorithm
# file: main.py
# author: steve flores
# description: game of connect 4 that allows the player to play against ai

# connect 4 boards are 7rowx6col
import random
import copy

ROW = 6
COL = 7
RED = 'X'
YELLOW = 'O'

# -----------------------
# x | x | x | x | x | x | x 
#---------------------------

# creates a new gameboard
def reset():
    board = []
    for i in range(ROW):
        nxtRow = []
        for j in range(COL):
            nxtRow.append('-')
        board.append(nxtRow)
    return board
    
# prints board to console
def printBoard(board):
    for i,row in enumerate(board):
        for j,col in enumerate(row):
            print("|{0}".format(board[i][j]),end='')
        print('|')

    print("",end=" ")
    for i in range(COL):
        print(i+1,end=" ")
    print()
        
# updates any given position on the board with x or o
def updateBoard(col,player,board):
    
    for i in range(ROW-1,-1,-1):
        if board[i][col] == '-':
            board[i][col] = player
            return
        
# allows player to make a move
def playerTurn(board):
    spot = None
    while True:
        spot = int(input("Input a number to drop your chip: "))
        spot -= 1
        if spot in range(0,COL):
            free = False
            for i in range(ROW):
                if '-' == board[i][spot]:
                    free = True
            if free:
                return spot
            else:
                print("invalid")
        else:
            print("Invalid")

# minimax algorithm that allows the AI player to "THINK"
def minimaxAI(board,player):
    # get first child boards
    nextMoves = addDepth(board,YELLOW)

    # calculate the cost of what each move is altering the depth with second param
    scores = []
    for bo,i in nextMoves:
        nxteval = getMaxEvalXboards(bo,3,RED)
        scores.append((nxteval,i))
    
    bestMove = min(scores)
    print(scores)
    print(bestMove)

    return bestMove[1]

# helper function that decides what the optimal moves are for the minimizing and maxamizing players
def getMaxEvalXboards(board,depth,player):
    if depth <= 0:
        return evalFct(board,player)
    
    xMoves = addDepth(board,player)
    
    # maximizing playesr turn
    maxEval=-10000
    minEval= 10000
    if player == RED:
        for (bo,i) in xMoves:
            tempVal = getMaxEvalXboards(bo,depth-1,YELLOW)
            if calculateWin(bo) == YELLOW:
                return -100000
            
            if tempVal > maxEval:
                maxEval = tempVal
        return maxEval
    #minimizing players turn
    else:
        for (bo,i) in xMoves:
            tempVal = getMaxEvalXboards(bo,depth-1,RED)
            if calculateWin(bo) == RED:
                return 100000
            
            if tempVal < minEval:
                minEval = tempVal
        return minEval

# evaluates any given win conditions on a given gameboard
def evalFct(board,player):
    redWins = 0
    yellowWins = 0

    checkWinner = calculateWin(board)
    if checkWinner == RED:
        return 10000
    if checkWinner == YELLOW:
        return -10000

    cols = checkCol(board)

    for i in cols:
        redCnt = i.count(RED)
        yllwCnt = i.count(YELLOW)
        if redCnt == 0:
            yellowWins+=1
        if yllwCnt == 0:
            redWins += 1

    rows = checkRow(board)
    for i in rows:
        redCnt = i.count(RED)
        yllwCnt = i.count(YELLOW)
        if redCnt == 0:
            yellowWins+=1
        if yllwCnt == 0:
            redWins += 1

    diag = checkDiag(board)

    for x in diag[0]:
        redCnt = x.count(RED)
        yllwCnt = x.count(YELLOW)
        
        if redCnt == 0:
            yellowWins+=1
        if yllwCnt == 0:
            redWins += 1        
        
    for y in diag[1]:
        redCnt = y.count(RED)
        yllwCnt = y.count(YELLOW)
        if redCnt == 0:
            yellowWins+=1
        if yllwCnt == 0:
            redWins += 1

    return redWins-yellowWins

# creates child boards from any given board position
def addDepth(board,player):
    potentialPositions = []
    
    # finds all open parts of the board
    for i in range(COL):
        hypoBoard = copy.deepcopy(board)
        updateBoard(i,player,hypoBoard)
        potentialPositions.append((hypoBoard,i))

    return potentialPositions

# checks for win 
def calculateWin(board):
    rows = checkRow(board)
    for currentRow in rows:
        if currentRow.count(RED) == 4:
            return RED
        elif currentRow.count(YELLOW) == 4:
            return YELLOW
    
    cols = checkCol(board)
    for currentCol in cols:
        if currentCol.count(RED) == 4:
            return RED
        elif currentCol.count(YELLOW) == 4:
            return YELLOW

    diags = checkDiag(board)

    for x in diags[0]:
        if x.count(RED) == 4:
            return RED
        elif x.count(YELLOW) == 4:
            return YELLOW
    for x in diags[1]:
        if x.count(RED) == 4:
            return RED
        elif x.count(YELLOW) == 4:
            return YELLOW
    return False


# helper function which grabs the columns
def checkCol(board):
    moveWindow = (ROW % 4) + 1
    
    cols = []
    for col in range(0,COL):

        for offset in range(0,moveWindow):
            cols.append([board[x+offset][col] for x in range(4)])
            
    return cols
# helper function which grabs the rows
def checkRow(board):
    moveWindow = (COL % 4)+1
        
    rows = []
    for row in range(0,ROW):

        for offset in range(0,moveWindow):
            rows.append([board[row][x+offset] for x in range(4)])

    return rows

# helper function which grabs the rows
def checkDiag(board):
    # 00 11 22 33 44 55
    # 10 21 32 43 54 
    # 30 41 52 63
    # order for going down the row

    diag1 = []
    diag2 = []
    # we can only get diagnlos from rowSize - 4 ex. 10-4=6 diagnols
    for i in range(ROW-3):
        
        topLeft = []
        topRight = []
        bottomLeft = []
        bottomRight = []
        for j in range(ROW-i):
            # goes down the ROWS
            topLeft.append(board[j+i][j])
            topRight.append(board[j+i][COL-j-1])
        
            bottomLeft.append(board[ROW-j-1][j])
            bottomRight.append(board[ROW-j-1][COL-j-1])
            
        diag1.append(topRight)
        diag1.append(bottomLeft)
        diag2.append(topLeft)
        diag2.append(bottomRight)


    newDiag1 = []
    for line in diag1:
        for size in range((len(line)%4)+1):
            window = line[size:size+4]
            newDiag1.append(window)
    
    newDiag2 = []
    for line in diag2:
        for size in range((len(line)%4)+1):
            window = line[size:size+4]
            newDiag2.append(window)
    
    return (newDiag1,newDiag2,diag1,diag2)
            

# main game loop
def play():
    turn = True
    gameBoard = reset()
    printBoard(gameBoard)

    while True:
        chipLocation = None
        
        if turn:
            chipLocation = playerTurn(gameBoard)
            updateBoard(chipLocation,RED,gameBoard)
        else:
            chipLocation = minimaxAI(gameBoard,YELLOW)
            # chipLocation = random.randint(0,COL-1)
            updateBoard(chipLocation,YELLOW,gameBoard)

        printBoard(gameBoard)
        winner = calculateWin(gameBoard)
        if winner == RED:
            print("Player wins!")
            break
        if winner == YELLOW:
            print("You Suck! Computer Wins!")
            break
        turn = not turn
        


if __name__ == '__main__':
    play()