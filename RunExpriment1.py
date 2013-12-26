from GameRunner import GameRunner, NO_LIMIT
from BlokusGameConstants import Players, GameOption
from BlokusGameInput import IllegalShapeFileFormatException
from BlokusGameState import BlokusGameState
from BlokusAgentSimple import BlokusAgentSimple
from BlokusAgentMcBoogerballs import BlokusAgentMcBoogerballs
'''
	Runing this script should output all of the raw information for experiment 1 as defined
	in the assignment specification doc.
	players compared should be defined each in a faile named 'BlokusAgent<choose the name>.py'.
	Output should be to file 'output1.txt' (or csv). 
	Alternatively, you may split the output into multiple files named 
	'output1_<a relevant name>.txt' (or csv).
'''

out = 'output1.txt' # (or csv)
#out_<...> = 'output1_<a relevant name>.txt' (or csv)

def game(player1, depth1, player2, depth2):
    player1 = player1(depth1)
    player2 = player2(depth2)

    (boardSize, orderedShapesMode, timeLimit) = GameOption[2]

    #timeLimit = NO_LIMIT
    
    agents = {}

    agents[Players.FIRST] = player1
    agents[Players.SECOND] = player2
    
    try:
        #if you want to use your own shapes file, send the path to it as the second parameter (instead of 'shapes.txt')
        state = BlokusGameState().setup(boardSize, 'shapes.txt', orderedShapesMode)
    except IllegalShapeFileFormatException:
        print '\nIllegal Shape File Format'
        return

    # print str(state)
    
    (winner, finalState) = (None, None)
    
    try:
        
        #if playing with interactive player put NO_LIMIT instead of timeLimit
        finalState = GameRunner(state, agents, timeLimit).run()
        winner = finalState.getWinner()
    
    except Exception as e:

        # print e
        winner = Players.FIRST if e.player == Players.SECOND else Players.SECOND

    if winner == Players.FIRST:
        return -1
    elif winner == Players.SECOND:
        return 1
    else:
        return 0

depths = [2]
RUNS = 1
table = {}
if __name__ == '__main__':
    for i in depths:
        for j in depths:
            table[('S', i, 'Y', j)] = { -1: 0, 0: 0, 1: 0 }
            table[('Y', i, 'S', j)] = { -1: 0, 0: 0, 1: 0 }
            if i != j:
                table[('S', i, 'S', j)] = { -1: 0, 0: 0, 1: 0 }
                table[('Y', i, 'Y', j)] = { -1: 0, 0: 0, 1: 0 }
            for run in range(RUNS):
                result = game(BlokusAgentMcBoogerballs, i, BlokusAgentSimple, j)
                table[('S', i, 'Y', j)][result] += 1
                result = game(BlokusAgentSimple, i, BlokusAgentMcBoogerballs, j)
                table[('Y', i, 'S', j)][result] += 1
                if i != j:
                    result = game(BlokusAgentSimple, i, BlokusAgentSimple, j)
                    table[('S', i, 'S', j)][result] += 1
                    result = game(BlokusAgentMcBoogerballs, i, BlokusAgentMcBoogerballs, j)
                    table[('Y', i, 'Y', j)][result] += 1

    print table
	# run experiment 1
	# output raw data to out file(s)
	
	# after runing, manually rename the output file(s) by adding '_results' before the file extension.
	# for example: output1_results.txt


