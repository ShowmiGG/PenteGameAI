# external libraries
from math import log, sqrt


#blueprint of a node
class Node:
    def __init__(self, state, action, playerWon = None):
        self.__state = state
        self.__wins = 0.0
        self.__visits = 0.0
        self.__playerWon = playerWon
        self.__action = action
        self.childNodes = []
        
    ################ Getters ################
    def __GetterState(self):
        return self.__state
    def __GetterWins(self):
        return self.__wins
    def __GetterVisits(self):
        return self.__visits
    def __GetterPlayerWon(self):
        return self.__playerWon
    def __GetterAction(self):
        return self.__action
    
    ############### Setters ##################
    def __SetterWins(self, value):
        self.__wins = value
    def __SetterVisits(self, value):
        self.__visits = value
    
    ################ Properties ###############
    state = property(fget=__GetterState)
    wins = property(fget=__GetterWins, fset=__SetterWins)
    visits = property(fget=__GetterVisits, fset=__SetterVisits)
    playerWon = property(fget=__GetterPlayerWon)
    action = property(fget=__GetterAction)
        
    
    #check if the current node is a leaf
    def IsLeaf(self):
        return(len(self.childNodes) == 0)
        
    #print the values of the node
#    def PrintValues(self):
#        print
#        print 'Board ==> '
#        print self.state.board
#        print 'Wins ==> '+ str(self.wins)
#        print 'Visits ==> '+ str(self.visits)
#        print 'PlayerWon ==> '+ str(self.playerWon)
#        print 'Action ==> ' + str(self.action)
#        actions = []
#        for node in self.childNodes:
#            actions.append(node.action)
#        print 'Child Nodes Actions ==>' + str(actions)
#        print

#blueprint of the UCT formula
class UCT:
    def __init__(self, game):
        self.__game = game
        self.__GameSettings = game.GameSettings
        self.tree = {}
        
    ################ Getters ################
    def __GetterGame(self):
        return self.__game
    def __GetterGameSettings(self):
        return self.GameSettings
    
    ################ Properties ###############
    game = property(fget=__GetterGame)
    Gamesettings = property(fget=__GetterGameSettings)
    
    #add a node to the tree
    def __AddNode(self, node):
        if not (node.state.ID in self.tree):
            self.tree[node.state.ID] = node
              
#    def PrintChildNodes(self, node):
#        print
#        print '##############################'
#        print '         Parent Node'
#        node.PrintValues()
#        print '         Child Nodes'
#        if node.childNodes:
#            for childNode in node.childNodes:
#                print childNode.PrintValues()
#        else:
#            print '          No child nodes'
#        print '##############################'
#        print
                
                
    # a recrusive method to perform a UCT search.
    def Search(self, currentNode):
        if currentNode.IsLeaf():
            # Expansion
            # expand the leaf node and create child nodes
            action = currentNode.state.GetAction()
            for expansion in range(self.__GameSettings.expansionNum):
                action = currentNode.state.GetAction()
                newState, playerWon = self.__game.SimStep(currentNode.state, action)
                newNode = Node(newState, action, playerWon)
                currentNode.childNodes.append(newNode)
                
            # Simulation
            # simulate from the game state the current node
            totalVisit = 0
            totalPlayerOneWon = 0
            for simulation in range(self.__GameSettings.simulationNum):
                for node in currentNode.childNodes:
                    state = node.state
                    while node.playerWon == None:
                        action = state.GetAction()
                        state, playerWon = self.__game.SimStep(state, action)
                        node.playerWon = playerWon
                    self.__UpdateNode(playerWon, node, totalVisit, totalPlayerOneWon)
                    if playerWon == 1:
                        totalPlayerOneWon += 1
                    totalVisit += 1
                
        else:
            # Selection
            # traverse throught the search tree to reach a leaf node
            maxUCBValue = -1
            bestChildNode = None
            for node in currentNode.childNodes:
                UCBValue = (node.wins/node.visits) + self.__GameSettings.C*sqrt(log(currentNode.visits)/node.visits)
                if UCBValue > maxUCBValue:
                    maxUCBValue = UCBValue
                    bestChildNode = node
            playerWon, totalVisit, totalPlayerOneWon = self.Search(bestChildNode)
            
        # Backpropagation
        # update the values of the route taken to reach the leaf node
        self.__UpdateNode(playerWon, currentNode, totalVisit, totalPlayerOneWon)
        self.__AddNode(currentNode)
#        print playerWon
#        print currentNode.state.turn
#        print totalVisit
#        print totalPlayerOneWon
        return playerWon, totalVisit, totalPlayerOneWon
#        return currentNode
    
    # update the values of the given node with the given values
    def __UpdateNode(self, playerWon, currentNode, totalVisit, totalPlayerOneWon):
        if currentNode.state.turn == playerWon:
            currentNode.wins += 1
            currentNode.visits += 1
        else:
            currentNode.visits += 1
        return currentNode
        