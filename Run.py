#import cProfile
#import pstats

from GameRunner import GameRunner, NO_LIMIT
from BlokusGameConstants import Players, GameOption
from BlokusGameInput import IllegalShapeFileFormatException
from BlokusGameState import BlokusGameState
from BlokusGameAgentExample import BlokusGameAgentExample
from BlokusAgentSimple import BlokusAgentSimple
from BlokusAgentMcBoogerballs import BlokusAgentMcBoogerballs
#from BlokusGameAgentInteractive import BlokusGameAgentInteractive

def go():
    
    (boardSize, orderedShapesMode, timeLimit) = GameOption[2]

    timeLimit = NO_LIMIT
    
    agents = {}

    agents[Players.FIRST] = BlokusAgentSimple(6)
    agents[Players.SECOND] = BlokusAgentMcBoogerballs(4)
#    agents[Players.FIRST] = BlokusGameAgentInteractive()
#    agents[Players.SECOND] = BlokusGameAgentInteractive()
    
    try:
        #if you want to use your own shapes file, send the path to it as the second parameter (instead of 'shapes.txt')
        state = BlokusGameState().setup(boardSize, 'shapes.txt', orderedShapesMode)
    except IllegalShapeFileFormatException:
        print '\nIllegal Shape File Format'
        return

    print str(state)
    
    (winner, finalState) = (None, None)
    
    try:
        
        #if playing with interactive player put NO_LIMIT instead of timeLimit
        finalState = GameRunner(state, agents, timeLimit).run()
        winner = finalState.getWinner()
    
    except Exception as e:

        print e
        winner = Players.FIRST if e.player == Players.SECOND else Players.SECOND
    
    finally:
        
        printFinalState(winner, finalState)

def printFinalState(winner, finalState):
    
    print '\nWinner:', winner
    
    if finalState:

        firstScore, firstColors = (finalState.currentPlayer.getScore(), finalState.currentPlayer.colors) if (finalState.currentPlayer.player == Players.FIRST) else (finalState.opponentPlayer.getScore(), finalState.opponentPlayer.colors)
        secondScore, secondColors = (finalState.currentPlayer.getScore(), finalState.currentPlayer.colors) if (finalState.currentPlayer.player == Players.SECOND) else (finalState.opponentPlayer.getScore(), finalState.opponentPlayer.colors)
    
        print '\n' + Players.FIRST + ' player\'s Points:', firstScore
        for color in firstColors:
            print '\n' + Players.FIRST + ' player\'s Color:', color.color
            print '\n' + Players.FIRST + ' player\'s Shapes Left:'
            for shape in color.shapes:
                print shape
        
        print '\n' + Players.SECOND + ' player\'s Points:', secondScore
        for color in secondColors:
            print '\n' + Players.SECOND + ' player\'s Color:', color.color
            print '\n' + Players.SECOND + ' player\'s Shapes Left:'
            for shape in color.shapes:
                print shape

go()

#you can remove the comments below and the relevant imports to profile your player and find some implementation "Bottlenecks" 

#profiler = cProfile.Profile()
#
#try:
#    profiler.runcall(go)
#finally:
#    stats = pstats.Stats(profiler)
#    stats.sort_stats("time")
#    stats.print_stats()
