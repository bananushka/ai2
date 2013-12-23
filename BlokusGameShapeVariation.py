class BlokusGameShapeVariation:
    
    def __init__(self, normal, binary, corners):
        self.normal = normal #(rows, columns, numOfSquares, locations)
        self.binary = binary
        self.corners = corners #indexes tuple of this shape's corners
        
    def __cmp__(self, other):
        return cmp(self.binary, other.binary)

    def __hash__(self):
        return hash(self.binary)
        
    def __str__(self):
        result = "\n"
        index = 0
        
        for _ in xrange(0, self.normal[0]):
            for _ in xrange(0, self.normal[1]):
                
                if index in self.normal[3]:
                    result += "*"
                else:
                    result += " "
            
                index += 1
            
            result += "\n"
        
        return result[:-1]

    def __repr__(self):
        return self.__str__()