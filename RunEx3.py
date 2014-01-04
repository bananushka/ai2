from GameRunner import GameRunner, NO_LIMIT
from BlokusGameConstants import *
from BlokusGameInput import IllegalShapeFileFormatException
from BlokusGameState import BlokusGameState
from BlokusAgentSimple import BlokusAgentSimple
from BlokusAgentMcBoogerballs import BlokusAgentMcBoogerballs, \
                                     TimeManagement, \
                                     Heuristics, \
                                     ChildrenOrdering, \
                                     SelectiveDeepening
from Runner import *
'''
	Runing this script should output all of the raw information for experiment 1 as defined
	in the assignment specification doc.
	players compared should be defined each in a faile named 'BlokusAgent<choose the name>.py'.
	Output should be to file 'output1.txt' (or csv).
	Alternatively, you may split the output into multiple files named 
	'output1_<a relevant name>.txt' (or csv).
'''

out = 'output3.txt' # (or csv)
#out_<...> = 'output1_<a relevant name>.txt' (or csv)


table = {}
if __name__ == '__main__':
    depths = [2]
    names = [ 'S', 'Y' ]

    args = [ Args.SIMPLE, addFeature(Args.SIMPLE, \
                childrenOrdering=ChildrenOrdering.HEURISTIC) ]
    times = [ 30, 40, 50, 60, 70 ]
    for time in times:
        options = [ { 'boardSize': BoardSize.FOURTEEN, \
                'timeLimit': time, \
                'orderedShapesMode': NOT_ORDERED_SHAPES_MODE } ]
        results = experiment(options, depths, args, runs=10)
        print csvResults(('output3-time-%s.csv' % time), results, names, depths, args)

    exit()

	
    params = [ \
            addFeature(Args.SIMPLE, \
                selectiveDeepening=SelectiveDeepening.HIGH_HEURISTICS), \
            addFeature(Args.SIMPLE, \
                childrenOrdering=ChildrenOrdering.HEURISTIC), \
            addFeature(Args.SIMPLE, \
                timeManagement=TimeManagement.MORE_TIME_AT_THE_BEGINNING), \
            addFeature(Args.SIMPLE, \
                timeManagement=TimeManagement.MORE_TIME_AT_THE_END) \
            ]


    for i, param in enumerate(params):
        args = [ Args.SIMPLE, param ]
        options = [ { 'boardSize': BoardSize.FOURTEEN, \
                'timeLimit': 30, \
                'orderedShapesMode': NOT_ORDERED_SHAPES_MODE } ]
        results = experiment(options, depths, args, runs=10)
        print csvResults(('output3-param-%s.csv' % i), results, names, depths, args)

	# after runing, manually rename the output file(s) by adding '_results' before the file extension.
	# for example: output1_results.txt


