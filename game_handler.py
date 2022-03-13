global game
global board
global delayRunning

# funtion for stopping computation after a certain delay(is called using threading.timer)
def stopComputation():
    global delayRunning
    delayRunning=False

def printGame():
    global game
    global board
    wasSeparated=[]
    for _ in range(len(board[0])):
        wasSeparated.append(False)
    # loop over all rows of board
    for rownum in range(len(board)):
        gamerow=game[rownum]
        boardrow=board[rownum]
        printstr = ""
        topstr = ""
        lastval = "0"
        # for every char from board list figure out if vertical seperation is needed -> insert "|" otherwise space
        for valuenum in range(len(boardrow)):
            boardvalue=boardrow[valuenum]
            gamevalue=gamerow[valuenum]
            lastSeparated=False
            if(boardvalue==lastval):
                printstr += " "+gamevalue
            else:
                printstr += "|"+gamevalue
                lastSeparated=True
            lastval=boardvalue
            #generate the row above this row by combining "-" and "+" to fit to grid
            if(rownum==0):
                if("0"==boardvalue):
                    if(wasSeparated[valuenum] or lastSeparated):
                        topstr+="+ "
                    else:
                        topstr+="  "
                else:
                    if(wasSeparated[valuenum] or lastSeparated):
                        topstr+="+—"
                    else:
                        topstr+="——"
            else:
                if(board[rownum-1][valuenum]==boardvalue):
                    if(wasSeparated[valuenum] or lastSeparated):
                        topstr+="+ "
                    else:
                        topstr+="  "
                else:
                    if(wasSeparated[valuenum] or lastSeparated):
                        topstr+="+—"
                    else:
                        topstr+="——"
            wasSeparated[valuenum]=lastSeparated
        print(topstr)
        print(printstr)

# function for importing .board files
def readBoard(boardfilepath):
    global game
    global board
    board = []
    game = []
    boardfile = open(boardfilepath,'r')
    # loop over rows
    for rowdata in boardfile.readlines():
        # row for board list
        row=[]
        # row for game list
        gamerow = []
        # append 0 for to make printing easier(cf. printBoard), does not affect game 
        rowdata+="0"
        # convert chars from file into 2d board list and create same size empty game list
        for char in rowdata:
            if(not char=='\n'):
                row.append(char)
                gamerow.append(" ")
        # append lists to board and game list
        board.append(row)
        game.append(gamerow)
    lastrow= []
    # add 0s for easier printing at the bottom
    for _ in range(len(row)):
        lastrow.append('0')
    board.append(lastrow)
    game.append(gamerow)

# function to modify game list to reflect a move made by a player
def makeMove(player,move):
    global game
    global board
    move=(int(move[0]),int(move[1]))
    if(game[move[1]][move[0]]==" " and (not board[move[1]][move[0]]=="0")):
        if(player=="max"):
            game[move[1]][move[0]]="a"
        else:
            game[move[1]][move[0]]="i"

# undo move -> no need to copy game list every time it is modified
def undoMove(move):
    global game
    global board
    move=(int(move[0]),int(move[1]))
    game[move[1]][move[0]]=" "

# generate a list of lists containing the coordinates of the spots corresponding to the seperate plates
def generateTilesInfo():
    global board
    tiles = []
    knownValues=[]
    for rownum in range(len(board)):
        row = board[rownum]
        for valuenum in range(len(row)):
            value=row[valuenum]
            if(not value=="0"):
                isKnown=False
                for testVal in knownValues:
                    if(testVal==value):
                        isKnown=True
                if(not isKnown):
                    tile = []
                    for testrownum in range(len(board)):
                        testrow = board[testrownum]
                        for testvaluenum in range(len(testrow)):
                            testvalue=testrow[testvaluenum]
                            if(testvalue==value):
                                tile.append((testvaluenum,testrownum))
                    tiles.append(tile)
                    knownValues.append(value)
    return tiles

# count points based on tilesInfo retrieved from above function
def countPoints(tilesInfo):
    global game
    count=0
    for tile in tilesInfo:
        tilecount=0
        for x,y in tile:
            x,y = int(x),int(y)
            if(game[y][x]=="a"):
                tilecount+=1
            elif(game[y][x]=="i"):
                tilecount-=1
        if(tilecount>0):
            count+=len(tile)
        elif(tilecount<0):
            count-=len(tile)
    return count

# get all possible moves given the last two moves and the game list
def possibleMoves(secLastX,secLastY,lastX,lastY):
    global game
    global board
    moves = []
    secLastX,secLastY,lastX,lastY=int(secLastX),int(secLastY),int(lastX),int(lastY)
    for testX in range(len(game[0])):
        if(game[lastY][testX]==" "):
            if(not board[lastY][testX]=="0"):
                if(not board[lastY][lastX]==board[lastY][testX]):
                    if(not board[secLastY][secLastX]==board[lastY][testX]):
                        moves.append((testX,lastY))
    for testY in range(len(game)):
        if(game[testY][lastX]==" "):
            if(not board[testY][lastX]=="0"):
                if(not board[lastY][lastX]==board[testY][lastX]):
                    if(not board[secLastY][secLastX]==board[testY][lastX]):
                        moves.append((lastX,testY))
    return moves
