from BlokusGameColor import BlokusGameColor

class BlokusGamePlayer():
    
    def setup(self, player, colors, shapes):
        self.player = player
        self.colors = []
        for color in colors:
            self.colors.append(BlokusGameColor().setup(color, shapes)) 
        self.currentColor = 0
        return self
    
    def copy(self):
        newPlayer = BlokusGamePlayer()
        newPlayer.player = self.player
        newPlayer.colors = [color.copy() for color in self.colors]
        newPlayer.currentColor = self.currentColor
        return newPlayer
    
    def getCurrentColor(self):
        return self.colors[self.currentColor]
    
    def endMove(self):
        self.currentColor = (self.currentColor + 1) % len(self.colors)
    
    def getScore(self):
        return sum([color.getScore() for color in self.colors])
    
    def getShapes(self):
        return [(color.color, color.shapes) for color in self.colors]
    
    def __cmp__(self, other):
        return cmp((self.player, tuple(self.colors), self.currentColor), (other.player, tuple(other.colors), other.currentColor))    
    
    def __hash__(self):
        return hash((self.player, tuple(self.colors), self.currentColor))

    def __str__(self):
        return self.player
    
    def __repr__(self):
        return self.__str__()