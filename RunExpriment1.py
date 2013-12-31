from GameRunner import GameRunner, NO_LIMIT
from BlokusGameConstants import Players, GameOption
from BlokusGameInput import IllegalShapeFileFormatException
from BlokusGameState import BlokusGameState
from BlokusAgentSimple import BlokusAgentSimple
from BlokusAgentMcBoogerballs import BlokusAgentMcBoogerballs, TimeManagement, Heuristics
from Runner import *
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


table = {}
if __name__ == '__main__':
    player1Args, player2Args = addDepth(depths=[2], \
            player1Args=[Args.SIMPLE], \
            player2Args=[ { 'heuristicType': Heuristics.SCORE | Heuristics.CORNERS } ])
    options = [ { 'timeLimit': NO_LIMIT } ]
    results1 = experiment(options, player1Args, player2Args)
    results2 = experiment(options, player2Args, player1Args)
    #showResults(results1, options, player1Args, player2Args)
    csvResults(results1, 'S', player1Args, 'Y', player2Args)
    #showResults(results2, options, player2Args, player1Args)

	
	# after runing, manually rename the output file(s) by adding '_results' before the file extension.
	# for example: output1_results.txt


