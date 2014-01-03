import sys
import traceback
from GameRunner import GameRunner, NO_LIMIT
from BlokusGameConstants import Players, GameOption
from BlokusGameInput import IllegalShapeFileFormatException
from BlokusGameState import BlokusGameState
from BlokusAgentMcBoogerballs import \
        BlokusAgentMcBoogerballs, \
        TimeManagement, \
        Heuristics

from cStringIO import StringIO


GAME_DEFAULTS = GameOption[2]
DEFAULT_RUNS = 20
DEFAULT_DEPTH = 2

class Args:
    SIMPLE = { 'heuristicType': Heuristics.SCORE }
    BASIC = { 'heuristicType': Heuristics.SCORE | Heuristics.ALL_CORNERS }

def showResults(results, options, player1Args, player2Args):
    for key, value in results.items():
        print '(%s, %s, %s) : First - %s, Second - %s, Tie - %s' % (options[key[0]], \
                                    player1Args[key[1]], \
                                    player2Args[key[2]], \
                                    value[-1], \
                                    value[1], \
                                    value[0])

def csvResults(filename, results, names, depths, args1, args2=[]):
    backup = sys.stdout # save original stdout

    sys.stdout = StringIO() # capture output
    if len(args2) == 0:
        args2 = args1

    for name in names:
        for depth in depths:
            sys.stdout.write(('\t,%s%s - Wins' % (name, depth)) \
                + ('\t,%s%s - Ties' % (name, depth)) \
                + ('\t,%s%s - Losses' % (name, depth)))


    for i, _1 in enumerate(args1):
        for depth1 in depths:
            print ''
            sys.stdout.write('%s%s' % (names[i], depth1))
            for j, _2 in enumerate(args2):
                for depth2 in depths:
                    sys.stdout.write('\t,%s,\t\t%s,\t\t%s\t' % ( results[(0, i, j, depth1, depth2)][-1], \
                                                results[(0, i, j, depth1, depth2)][0], \
                                                results[(0, i, j, depth1, depth2)][1]))

    print
    out = sys.stdout.getvalue() # release output
    f = open(filename, 'w')
    f.write(out)
    f.close()

    sys.stdout.close() # close the stream 
    sys.stdout = backup # restore original stdout
    return out

def addDepth(depths=[DEFAULT_DEPTH], \
                        player1Args=[Args.SIMPLE]):
    player1ArgsWithDepth = []
    for depth in depths:
        for args in player1Args:
            argsCopy = args.copy()
            argsCopy.update({'depth': depth})
            player1ArgsWithDepth.append(argsCopy)

    return player1ArgsWithDepth

def addFeature(args, **features):
    argsCopy = args.copy()
    for key, value in features.iteritems():
        argsCopy[key] = value

    return argsCopy

def experiment(options=[{}], depths=[DEFAULT_DEPTH], \
                player1Args=[Args.SIMPLE], player2Args=[], 
                runs=DEFAULT_RUNS):
    if len(player2Args) == 0:
        player2Args = player1Args
    results = {}
    for i, gameOptions in enumerate(options):
        for j, args1 in enumerate(player1Args):
            for k, args2 in enumerate(player2Args):
                for depth1 in depths:
                    for depth2 in depths:
                        results[(i, j, k, depth1, depth2)] = \
                                { -1: 0, 0: 0, 1: 0 }
                        if j == k and depth1 == depth2:
                            continue
                        for run in range(runs):
                            args1Copy = args1.copy()
                            args1Copy['depth'] = depth1
                            args2Copy = args2.copy()
                            args2Copy['depth'] = depth1
                            result = singleGame(gameOptions, args1Copy, args2Copy)
                            results[(i, j, k, depth1, depth2)][result] += 1

    return results

def singleGame(gameOptions, player1Args, player2Args):
    player1 = BlokusAgentMcBoogerballs(**player1Args)
    player2 = BlokusAgentMcBoogerballs(**player2Args)

    boardSize = gameOptions.get('boardSize', GAME_DEFAULTS[0])
    orderedShapesMode = gameOptions.get('orderedShapesMode', GAME_DEFAULTS[1])
    timeLimit = gameOptions.get('timeLimit', GAME_DEFAULTS[2])

    agents = {\
            Players.FIRST: player1,\
            Players.SECOND: player2\
            }

    try:
        state = BlokusGameState().setup(boardSize, 'shapes.txt',\
                orderedShapesMode)

    except IllegalShapeFileFormatException:
        print '\nIllegal shape file format'
        return

    winner, finalState = None, None

    try:
        finalState = GameRunner(state, agents, timeLimit).run()
        winner = finalState.getWinner()
    except Exception as e:
        print e
        print traceback.format_exc()

    if winner == Players.FIRST:
        return -1
    elif winner == Players.SECOND:
        return 1
    else:
        return 0


    



