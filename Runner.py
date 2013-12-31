import sys
from GameRunner import GameRunner, NO_LIMIT
from BlokusGameConstants import Players, GameOption
from BlokusGameInput import IllegalShapeFileFormatException
from BlokusGameState import BlokusGameState
from BlokusAgentMcBoogerballs import \
        BlokusAgentMcBoogerballs, \
        TimeManagement, \
        Heuristics


GAME_DEFAULTS = GameOption[2]
DEFAULT_RUNS = 5
DEFAULT_DEPTH = 2

class Args:
    SIMPLE = { 'heuristicType': Heuristics.SCORE }

def showResults(results, options, player1Args, player2Args):
    for key, value in results.items():
        print '(%s, %s, %s) : First - %s, Second - %s, Tie - %s' % (options[key[0]], \
                                    player1Args[key[1]], \
                                    player2Args[key[2]], \
                                    value[-1], \
                                    value[1], \
                                    value[0])

def csvResults(results, player1Name, player1Args, player2Name, player2Args):
    print player2Args
    for i, args2 in enumerate(player2Args):
        print ('\t,%s%s Wins' % (player2Name, args2['depth'])) \
                + ('\t,%s%s Ties' % (player2Name, args2['depth'])) \
                + ('\t,%s%s Loses' % (player2Name, args2['depth']))

    for i, args1 in enumerate(player1Args):
        sys.stdout.write('%s%s' % (player1Name, args1['depth']))
        for j, args2 in enumerate(player2Args):
            print '\t,%s,\t%s,\t%s' % ( results[(0, i, j)][-1], \
                                        results[(0, i, j)][0], \
                                        results[(0, i, j)][1])




def addDepth(depths=[DEFAULT_DEPTH], \
                        player1Args=[Args.SIMPLE], player2Args=[]):
    player1ArgsWithDepth = []
    player2ArgsWithDepth = []
    if len(player2Args) == 0:
        player2Args = player1Args
    for depth in depths:
        for args in player1Args:
            argsCopy = args.copy()
            argsCopy.update({'depth': depth})
            player1ArgsWithDepth.append(argsCopy)
        for args in player2Args:
            argsCopy = args.copy()
            argsCopy.update({'depth': depth})
            player2ArgsWithDepth.append(argsCopy)

    return player1ArgsWithDepth, player2ArgsWithDepth

def experiment(options=[{}], \
                player1Args=[Args.SIMPLE], player2Args=[], 
                runs=DEFAULT_RUNS):
    if len(player2Args) == 0:
        player2Args = player1Args
    results = {}
    for i, gameOptions in enumerate(options):
        for j, args1 in enumerate(player1Args):
            for k, args2 in enumerate(player2Args):
                results[(i, j, k)] = \
                        { -1: 0, 0: 0, 1: 0 }
                for run in range(runs):
                    result = singleGame(gameOptions, args1, args2)
                    results[(i, j, k)][result] += 1

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

    except IllegalShapesFileFormatException:
        print '\nIllegal shape file format'
        return

    winner, finalState = None, None

    try:
        finalState = GameRunner(state, agents, timeLimit).run()
        winner = finalState.getWinner()
    except Exception as e:
        print e

    if winner == Players.FIRST:
        return -1
    elif winner == Players.SECOND:
        return 1
    else:
        return 0


    



