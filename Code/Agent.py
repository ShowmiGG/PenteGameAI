# user defined modules
import UCT as uctPackage
import Config as cfg

#blueprint of a human player
class Human:
    def __init__(self, name):
        self.__name = name
        self.__capturedPairs = 0
        self.__steps = 0
    
    ################ Getters ################
    def __GetterName(self):
        return self.__name
    def __GetterCapturedPairs(self):
        return self.__capturedPairs
    def __GetterSteps(self):
        return self.__steps
    
    ############### Setters ##################
    def __SetterCapturedPairs(self, value):
        self.__capturedPairs = value
    def __SetterSteps(self, value):
        self.__steps = value
    
    ################ Properties ###############
    name = property(fget=__GetterName)
    capturedPairs = property(fget=__GetterCapturedPairs, fset=__SetterCapturedPairs)
    steps = property(fget=__GetterSteps, fset=__SetterSteps)
        
    #allows the human player to make an action
    def GetAction(self, node = None):
        while True:
            try:
                column = raw_input('Column ' + cfg.USERINPUT)
                row = raw_input('Row ' + cfg.USERINPUT)
                action = [int(column), int(row)]
                break
            except:
                print "Invalid input"
        return action

#blueprint of a computer player
class Agent(Human):
    def __init__(self, name, game):
        Human.__init__(self, name)
        self.__game = game
        self.__UCT = uctPackage.UCT(self.__game)
    
    
    #allows the computer player to make an action
    def GetAction(self, node):
        print 'Processing...'
        if node.state.ID in self.__UCT.tree:
            node = self.__UCT.tree[node.state.ID]
        for playout in range(self.__game.GameSettings.playoutNum):
            #self.UCT.RunUCT(node)
            self.__UCT.Search(node)
        bestNodeVisits = -float('inf')
        bestNode = None
        for childNode in node.childNodes:
            if childNode.visits > bestNodeVisits:
                bestNodeVisits = childNode.visits
                bestNode = childNode
        action = bestNode.action
        #self.UCT.PrintChildNodes(node)
        return action
        
        