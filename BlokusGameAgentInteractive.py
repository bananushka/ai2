from GameAgent import GameAgent

class BlokusGameAgentInteractive(GameAgent):
    
    def setup(self, player, state, timeLimit):        
        self.player = player
        
    def move(self, state):
        
        actions = []
        actionsOnScreen = False
        
        while True:
            
            print self.player + ' player\'s turn. choose move:\n'
            
            index = 0
            
            if not actionsOnScreen:
                actions = [action for action in state.getSuccessors().iterkeys()]
                actions.sort(key = lambda action: action.location)
                for action in actions:
                    print index, ":", action,'\n'
                    index += 1
                actionsOnScreen = True

            inp = raw_input('your selection: ')
            actionParams = inp.split()
     
            try:
                if ((len(actionParams) != 1) or (int(actionParams[0]) >= len(actions)) or (int(actionParams[0]) < 0)):
                    print "Bad format\n"
                    continue            
            except:
                print "Bad format\n"
                continue            
                                
            index = int(actionParams[0])
            action = actions[index]
            
            return action  