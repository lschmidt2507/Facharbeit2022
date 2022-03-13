import threading
import time
import math
from game_handler import printGame,generateTilesInfo,countPoints,readBoard,makeMove,undoMove,possibleMoves

maxTime=30

global delayRunning

# funtion for stopping computation after a certain delay(is called using threading.timer)
def stopComputation():
    global delayRunning
    delayRunning=False
    print("done!")

#actual minimax algorithm
def minimax(depth,tilesInfo,alpha,beta,player,secLastX,secLastY,lastX,lastY,initcall):
    global game
    global board
    global delayRunning
    moves=possibleMoves(secLastX,secLastY,lastX,lastY)
    totalEvaluations=0

    # check if max depth reached or final game state and return evaluation if true
    if(depth==0 or len(moves)==0):
        # count point while adding decimal places to prefer longer games as the opponent has more opportunities to fail + return total evaluations 1
        if(initcall):
            return countPoints(tilesInfo)+depth/100,0,1
        else:
            return countPoints(tilesInfo)+depth/100,1
    #check if delay running
    if(not delayRunning):
        if(initcall):
            return 0,0,0
        else:
            return 0,0
    else:
        # maximizing player's turn
        if(player=="max"):            
            maxEval=-1000
            #try every possible move
            for move in moves:
                # make move and evaluate by calling recursively
                makeMove(player,move)
                evalu, evaluationNum=minimax(depth-1,tilesInfo,alpha,beta,"min",lastX,lastY,move[0],move[1],False)
                totalEvaluations+=evaluationNum
                # undo move
                undoMove(move)
                # update bestmove and best evaluation
                if(evalu>maxEval):
                    maxEval=evalu
                    bestmove=move
                alpha=max(alpha,evalu)
                if(beta<=evalu):
                    break
            # if initial call return recommended move and check if delayrunning
            if(initcall):
                if(delayRunning):
                    return maxEval,bestmove, totalEvaluations
                else:
                    return 0,0,0
            else:
                return maxEval, totalEvaluations
        else:
            #min player's turn
            minEval=1000
            #try every possible move
            for move in moves:
                # make move and evaluate by calling recursively
                makeMove(player,move)
                evalu,evaluationNum=minimax(depth-1,tilesInfo,alpha,beta,"max",lastX,lastY,move[0],move[1],False)
                totalEvaluations+=evaluationNum
                # undo move
                undoMove(move)
                # update bestmove and best evaluation
                if(evalu<minEval):
                    minEval=evalu
                    bestmove=move
                beta=min(beta,evalu)
                if(evalu<=alpha):
                    break
            # if initial call return recommended move check if delayRunning
            if(initcall):
                if(delayRunning):
                    return minEval,bestmove, totalEvaluations
                else:
                    return 0,0,0
            else:
                return minEval, totalEvaluations

# read .board file and intilize global board and game variable
readBoard("./board.table")

tilesInfo=generateTilesInfo()

# make some arbitrary moves
makeMove("min",(2,0))
makeMove("max",(2,3))
makeMove("min",(5,3))
makeMove("max",(5,0))
makeMove("min",(3,0))
# set last move data
lastX=4
secLastX=4
lastY=3
secLastY=0

#start timer
delayRunning=True
threading.Timer(maxTime,stopComputation).start()
depth=1

# run while time left
while(delayRunning):
    # call minimax with current depth
    startTime = time.time()
    tempevalu,tempmove,totalEvaluations = minimax(depth,tilesInfo,-1000,1000,"max",secLastX,secLastY,lastX,lastY,True)
    endTime = time.time()
    # check if was interrupted(returns 0)
    if(not tempmove==0):
        try:
            print(f"{depth} & {totalEvaluations} & {round(math.exp(math.log(totalEvaluations)/depth),2)} & {round(endTime-startTime,2)} & {round(totalEvaluations/round(endTime-startTime,2),2)}")
        except Exception as e:
            print(f"{depth} & {totalEvaluations} & {round(math.exp(math.log(totalEvaluations)/depth),2)} & {round(endTime-startTime,2)} & -")
    # increase depth
    depth+=1