from GameRunner import GameRunner, NO_LIMIT
from BlokusGameConstants import Players, GameOption
from BlokusGameInput import IllegalShapeFileFormatException
from BlokusGameState import BlokusGameState
from BlokusAgentSimple import BlokusAgentSimple
from BlokusAgentMcBoogerballs import BlokusAgentMcBoogerballs, TimeManagement, Heuristics
from Runner import *
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


if __name__ == '__main__':
    depths = [2]
    names = [ 'S', 'Y' ]
    args = [Args.SIMPLE, {
                    'heuristicType': Heuristics.SCORE | Heuristics.ALL_CORNERS
                }]
    playerArgs = addDepth(depths=depths, player1Args=args)
    options = [ {} ]
    results = experiment(options, depths, playerArgs)
    print csvResults(out, results, names, depths, playerArgs)
