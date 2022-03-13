import threading
from game_handler import stopComputation,printGame,generateTilesInfo,countPoints,readBoard,makeMove,undoMove,possibleMoves

starttiefe=1
bedenkzeit=10
assist=False

#actual minimax algorithm
def minimax(tiefe,tilesInfo,alpha,beta,player,secLastX,secLastY,lastX,lastY,initcall):
    global game
    global board
    global delayRunning
    moves=possibleMoves(secLastX,secLastY,lastX,lastY)

    # check to see if time left for computation, otherwise immediately return 0
    if(not delayRunning):
        if(initcall):
            return 0,0
        else:
            return 0
    # check if max depth reached or final game state and return evaluation if true
    if(tiefe==0 or len(moves)==0):
        # count point while adding decimal places to prefer lolnger games as the opponent has more opportunities to fail
        if(initcall):
            return countPoints(tilesInfo)+tiefe/100,0
        else:
            return countPoints(tilesInfo)+tiefe/100
        
    else:
        # maximizing player's turn
        if(player=="max"):            
            maxEval=-1000
            #try every possible move
            for move in moves:
                # make move and evaluate by calling recursively
                makeMove(player,move)
                evalu=minimax(tiefe-1,tilesInfo,alpha,beta,"min",lastX,lastY,move[0],move[1],False)
                # undo move
                undoMove(move)
                # update bestmove and best evaluation
                if(evalu>maxEval):
                    maxEval=evalu
                    bestmove=move
                alpha=max(alpha,evalu)
                if(beta<=evalu):
                    break
            # if initial call return recommended move
            if(initcall):
                return maxEval,bestmove
            else:
                return maxEval
        else:
            #min player's turn
            minEval=1000
            #try every possible move
            for move in moves:
                # make move and evaluate by calling recursively
                makeMove(player,move)
                evalu=minimax(tiefe-1,tilesInfo,alpha,beta,"max",lastX,lastY,move[0],move[1],False)
                # undo move
                undoMove(move)
                # update bestmove and best evaluation
                if(evalu<minEval):
                    minEval=evalu
                    bestmove=move
                beta=min(beta,evalu)
                if(evalu<=alpha):
                    break
            # if initial call return recommended move
            if(initcall):
                return minEval,bestmove
            else:
                return minEval

readBoard("./board.table")
tilesInfo=generateTilesInfo()

#first move
move=(str(input("x-coord:")),str(input("y-coord:")))
makeMove("min",move)
lastX=move[0]
secLastX=move[0]
lastY=move[1]
secLastY=move[1]
#while moves left
while len(possibleMoves(secLastX,secLastY,lastX,lastY))>0:

    #start timer
    delayRunning=True
    threading.Timer(bedenkzeit,stopComputation).start()
    tiefe=starttiefe
    while(delayRunning):
        tempevalu,tempmove = minimax(tiefe,tilesInfo,-1000,1000,"max",secLastX,secLastY,lastX,lastY,True)
        if(not tempmove==0):
            evalu, move = tempevalu, tempmove
        tiefe+=1
    #output
    print("reached depth "+str(tiefe-1))
    print("making move "+str(move)+" with evaluation "+str(evalu))
    makeMove("max",move)
    # update last moves
    secLastX=lastX
    secLastY=lastY
    lastX=move[0]
    lastY=move[1]
    #output
    printGame()
    print(countPoints(tilesInfo))
    print(possibleMoves(secLastX,secLastY,lastX,lastY))
    # check if sill moves remaining
    if(len(possibleMoves(secLastX,secLastY,lastX,lastY))<0):
        break
    # if assistance is turned on the optimal move will be calculated and given to the player
    if(assist):
        delayRunning=True
        threading.Timer(bedenkzeit,stopComputation).start()
        tiefe=starttiefe
        while(delayRunning):
            tempevalu,tempmove = minimax(tiefe,tilesInfo,-1000,1000,"min",secLastX,secLastY,lastX,lastY,True)
            if(not tempmove==0):
                evalu, move = tempevalu, tempmove
            tiefe+=1
        print("recommended move: "+str(move))
    # get player move
    move=(str(input("x-coord:")),str(input("y-coord:")))
    makeMove("min",move)
    secLastX=lastX
    secLastY=lastY
    lastX=move[0]
    lastY=move[1]
# determine winner
if(countPoints(tilesInfo)<0):
    print("Sieg Spieler")
elif(countPoints(tilesInfo)==0):
    print("Unentschieden")
else:
    print("Minimax gewinnt")