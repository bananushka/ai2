from GameRunner import GameRunner, NO_LIMIT
from BlokusGameConstants import Players, GameOption
from BlokusGameInput import IllegalShapeFileFormatException
from BlokusGameState import BlokusGameState
from BlokusAgentSimple import BlokusAgentSimple
from BlokusAgentMcBoogerballs import BlokusAgentMcBoogerballs, TimeManagement, Heuristics
from RunExpriment2 import game
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


depths = [2]
RUNS = 3
TIME = 60
table = {}
if __name__ == '__main__':
    for i in depths:
        for j in depths:
            table[('YC', i, 'S', j)] = { -1: 0, 0: 0, 1: 0 }
            table[('YP', i, 'S', j)] = { -1: 0, 0: 0, 1: 0 }
            table[('YC+P', i, 'S', j)] = { -1: 0, 0: 0, 1: 0 }
            table[('YCS+P', i, 'S', j)] = { -1: 0, 0: 0, 1: 0 }
            if i != j:
                table[('S', i, 'S', j)] = { -1: 0, 0: 0, 1: 0 }
                table[('Y', i, 'Y', j)] = { -1: 0, 0: 0, 1: 0 }
            for run in range(RUNS):
                result = game(TIME, BlokusAgentMcBoogerballs, i, BlokusAgentSimple, j, \
                        { 'heuristicType': Heuristics.CORNERS })
                table[('YC', i, 'S', j)][result] += 1
                result = game(TIME, BlokusAgentMcBoogerballs, i, BlokusAgentSimple, j, \
                        { 'heuristicType': Heuristics.PARENT })
                table[('YP', i, 'S', j)][result] += 1
                #result = game(TIME, BlokusAgentSimple, i, BlokusAgentMcBoogerballs, j)
                result = game(TIME, BlokusAgentMcBoogerballs, i, BlokusAgentSimple, j, \
                        {'heuristicType': Heuristics.CORNERS | Heuristics.PARENT})
                table[('YC+P', i, 'S', j)][result] += 1
                result = game(TIME, BlokusAgentMcBoogerballs, i, BlokusAgentSimple, j, \
                        {'heuristicType': Heuristics.CORNERS_TIMES_SQUARES | Heuristics.PARENT })
                table[('YCS+P', i, 'S', j)][result] += 1
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


