'''
	This file is your implementation of a Blokus Playing Agent for the tournament.
	- Change ids to your own.
	- Choose a name for your AI player.
	- Don't forget to create your shapes file by the name specified.
	- Implement the two functions move() and setup().	
'''

from GameAgent import GameAgent

class BlokusCompetitionAgent (GameAgent):
	ids = ('300923000', '305625626') # insert your ID numbers here instead.
	# ids = '012345678'			 # In case you are a single submitter.
	
	agentName = 'AI_' + str(ids[0][-2:]) + '_' + str(ids[1][-2:])
				# replace this name with any nice name you choose for your AI player
	
	shapesFile = 'TournamentShapes.txt' 
					# Create the shapes file used in the tournament by this name
					# Do not change the name defined here

	def move(self, gameState):
		'''
		This is the method called by the runner of this agent.
		It includes the code that decides the next move.

		@param gameState: The current game state.
		@return: The GameAction that the agent will execute in its next move.
		'''
		raise NotImplementedError()    

	def setup(self, player, gameState, timeLimit):
		'''
		This is method is called once at the beginning of the game, 
		and enables the agent to prepare for things to come.

		@param player: Your player.
		@param gameState: The initial game state.
		@param timeLimit: The time that will be allocated for a game.
		'''
		raise NotImplementedError()		
