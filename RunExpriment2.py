from GameRunner import GameRunner, NO_LIMIT
from BlokusGameConstants import Players, GameOption
from BlokusGameInput import IllegalShapeFileFormatException
from BlokusGameState import BlokusGameState
from BlokusAgentSimple import BlokusAgentSimple
from BlokusAgentMcBoogerballs import BlokusAgentMcBoogerballs, TimeManagement
'''
	Runing this script should output all of the raw information for experiment 2
	as defined in the assignment specification doc.
	Input shape files are 10 files you are required to write named shapes<i>.txt, following
	the format of the supplied shapes.txt and complying with the constraints defined in the
	assignment specification  document.
	Use the function makeShapes() in BlokusGameInput.py to ensure compliance.
	players compared should be defined each in a faile named 'BlokusAgent<choose the name>.py'.	
	Output should be to the file 'output2.txt' (or csv). 
	Alternatively, you may split the output into multiple files named 
	'output2_<a relevant name>.txt' (or csv).
'''

inShapes = ['shapes' + str(i) + '.txt' for i in xrange(1,11)]

out = 'output2.txt' # (or csv)
#out_<...> = 'output2_<a relevant name>.txt' (or csv)

def game(timeLimit, player1, depth1, player2, depth2, player1args={}, player2args={}):
    player1 = player1(depth1, **player1args)
    player2 = player2(depth2, **player2args)

    (boardSize, orderedShapesMode, _) = GameOption[2]

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
    except IllegalShapeFileFormatException:
        pass
    
    '''
    except Exception as e:
        print e

        # print e
        winner = Players.FIRST if e.player == Players.SECOND else Players.SECOND
        '''

    if winner == Players.FIRST:
        return -1
    elif winner == Players.SECOND:
        return 1
    else:
        return 0

depths = [2, 3, 4]
limits = range(20, 200, 20)
RUNS = 10
table = {}
if __name__ == '__main__':
    for i in depths:
        for limit in limits:
            table[(i, 'S', 'Y', limit)] = { -1: 0, 0: 0, 1: 0 }
            table[(i, 'Y', 'S', limit)] = { -1: 0, 0: 0, 1: 0 }
            for run in range(RUNS):
                result = game(BlokusAgentMcBoogerballs, i, BlokusAgentMcBoogerballs, i,\
                        { 'timeMangement': TimeManagement.MORE_TIME_AT_THE_END })
                table[(i, 'S', 'Y', limit)][result] += 1 
                result = game(BlokusAgentMcBoogerballs, i, BlokusAgentMcBoogerballs, i,\
                        {}, { 'timeManagement': TimeManagement.MORE_TIME_AT_THE_END })
                table[(i, 'Y', 'S', limit)][result] += 1 

    print table
	# run experiment 1
	# output raw data to out file(s)
	
	# after runing, manually rename the output file(s) by adding '_results' before the file extension.
	# for example: output1_results.txt


