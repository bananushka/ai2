from GameRunner import GameRunner, NO_LIMIT
from BlokusGameConstants import Players, GameOption
from BlokusGameInput import IllegalShapeFileFormatException
from BlokusGameState import BlokusGameState
from BlokusAgentSimple import BlokusAgentSimple
from BlokusAgentMcBoogerballs import \
        BlokusAgentMcBoogerballs, \
        TimeManagement, \
        Heuristics, \
        SelectiveDeepening, \
        ChildrenOrdering
from Runner import *
'''
	Runing this script should output all of the raw information for experiment 2
	as defined in the assignment specification doc.
	Input shape files are 5 files you are required to write named shapes<i>.txt, following
	the format of the supplied shapes.txt and complying with the constraints defined in the
	assignment specification  document.
	Use the function makeShapes() in BlokusGameInput.py to ensure compliance.
	players compared should be defined each in a faile named 'BlokusAgent<choose the name>.py'.	
	Output should be to the file 'output2.txt' (or csv). 
	Alternatively, you may split the output into multiple files named 
	'output2_<a relevant name>.txt' (or csv).
'''

inShapes = ['shapes' + str(i) + '.txt' for i in xrange(1,11)]

out = 'output2.csv' # (or csv)
#out_<...> = 'output2_<a relevant name>.txt' (or csv)


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
        print csvResults(('output2-time-%s.csv' % time), results, names, depths, args)

