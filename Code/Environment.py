# external libraries
import random
import time
import numpy as np

#blueprint for the game state object
class GameState:
    def __init__(self, board, turn, capturedPlayer1Pairs, capturedPlayer2Pairs, GameSettings):
        self.__GameSettings = GameSettings
        self.__board = board
        self.__turn = turn
        self.__capturedPlayer1Pairs = capturedPlayer1Pairs
        self.__capturedPlayer2Pairs = capturedPlayer2Pairs
        self.__ID = self.__GetStateID(self.board)
        
    ################ Getters ################
    def __GetterGameSettings(self):
        return self.__GameSettings
    def __GetterBoard(self):
        return self.__board
    def __GetterTurn(self):
        return self.__turn
    def __GetterCapturedPlayer1Pairs(self):
        return self.__capturedPlayer1Pairs
    def __GetterCapturedPlayer2Pairs(self):
        return self.__capturedPlayer2Pairs
    def __GetterID(self):
        return self.__ID
    
    ################ Properties ###############
    GameSettings = property(fget=__GetterGameSettings)
    board = property(fget=__GetterBoard)
    turn = property(fget=__GetterTurn)
    capturedPlayer1Pairs = property(fget=__GetterCapturedPlayer1Pairs)
    capturedPlayer2Pairs = property(fget=__GetterCapturedPlayer2Pairs)
    ID = property(fget=__GetterID)
    
    # create an ID for the game state based on the current game board
    def __GetStateID(self, board):
        return ''.join(str(int(x)) for x in board.flatten())
        
    # get all the valid actions in the current game state
    def GetValidActions(self):
        validActions = []
        for i in range(self.GameSettings.boardSideLength):
            for j in range(self.GameSettings.boardSideLength):
                currentAction = [i, j]
                if (self.board[j][i] == self.GameSettings.blankSpaceSymbol):
                    validActions.append(currentAction)
        return validActions
    
    # get action to be used for the simulation in the UCT process based on the game difficulty
    def GetAction(self):
        validActions = self.GetValidActions()
        actions = []
        
        if self.GameSettings.mode == 'Normal':
            for action in validActions:
                if self.__IsImportantAction(self.board, action, 2):
                    actions.append(action)
                
        elif self.GameSettings.mode == 'Hard':
            for action in validActions:
                if self.__IsImportantAction(self.board, action, 3):
                    actions.append(action)
            if not actions:
                for action in validActions:
                    if self.__IsImportantAction(self.board, action, 2):
                        actions.append(action)
                
                
        if not actions:
            for action in validActions:
                if self.__IsImportantAction(self.board, action, 1):
                    actions.append(action)
        if not actions:
            actions = validActions
        
        actionIndex = random.randint(0, len(actions)-1)
        action = actions[actionIndex]
        
        self.GameSettings.expansionNum = len(actions)
        
        return action
    
    # get the number of identical stones connected to an space on the board
    # it returns true if the number of stones connected is longer than the length given
    def __IsImportantAction(self, board, action, connectionLength):
        i = action[1]
        j = action[0]
        numOfStonesConnectedList = []
        
        # calculate the total number of horizontally connected stones
        numOfStonesConnected  = self.__GetHorizontalConnectedStones(board, self.GameSettings.playerOneStoneSymbol, i, j)
        numOfStonesConnectedList.append(numOfStonesConnected)
        numOfStonesConnected  = self.__GetHorizontalConnectedStones(board, self.GameSettings.playerTwoStoneSymbol, i, j)
        numOfStonesConnectedList.append(numOfStonesConnected)
        
        # calculate the total number of vertically connected stones
        numOfStonesConnected  = self.__GetVerticalConnectedStones(board, self.GameSettings.playerOneStoneSymbol, i, j)
        numOfStonesConnectedList.append(numOfStonesConnected)
        numOfStonesConnected  = self.__GetVerticalConnectedStones(board, self.GameSettings.playerTwoStoneSymbol, i, j)
        numOfStonesConnectedList.append(numOfStonesConnected)
        
        # calculate the total number of \ diagonally connected stones
        numOfStonesConnected  = self.__GetFirstDiagonalConnectedStones(board, self.GameSettings.playerOneStoneSymbol, i, j)
        numOfStonesConnectedList.append(numOfStonesConnected)
        numOfStonesConnected  = self.__GetFirstDiagonalConnectedStones(board, self.GameSettings.playerTwoStoneSymbol, i, j)
        numOfStonesConnectedList.append(numOfStonesConnected)
        
        # calculate the total number of / diagonally connected stones
        numOfStonesConnected  = self.__GetSecondDiagonalConnectedStones(board, self.GameSettings.playerOneStoneSymbol, i, j)
        numOfStonesConnectedList.append(numOfStonesConnected)
        numOfStonesConnected  = self.__GetSecondDiagonalConnectedStones(board, self.GameSettings.playerTwoStoneSymbol, i, j)
        numOfStonesConnectedList.append(numOfStonesConnected)
        
        # return true if the total number of connected stones in any direction 
        # is long enough to be considered as important action
        for numOfStonesConnected in numOfStonesConnectedList:
            if numOfStonesConnected >= connectionLength:
                return True
    
    # get the number of identical connected horizontal stones
    def __GetHorizontalConnectedStones(self, board, testStone,  i, j):
        numOfStonesConnected = 0
            
        current_i = i-1
        current_j = j
        if current_i >= 0:
            while board[current_i][current_j] != self.GameSettings.blankSpaceSymbol:
                if board[current_i][current_j] == testStone:
                    numOfStonesConnected += 1
                else:
                    break
                if not current_i-1 >= 0:
                    break
                current_i -= 1
        
        current_i = i+1
        if current_i < self.GameSettings.boardSideLength:
            while board[current_i][current_j] != self.GameSettings.blankSpaceSymbol:
                if board[current_i][current_j] == testStone:
                    numOfStonesConnected += 1
                else:
                    break
                if not current_i+1 < self.GameSettings.boardSideLength:
                    break
                current_i += 1
        return numOfStonesConnected
    
    # get the number of identical connected vertical stones
    def __GetVerticalConnectedStones(self, board, testStone, i, j):
        numOfStonesConnected = 0
        
        current_i = i
        current_j = j-1
        if current_j >= 0:
            while board[current_i][current_j] != self.GameSettings.blankSpaceSymbol:
                if board[current_i][current_j] == testStone:
                    numOfStonesConnected += 1
                else:
                    break
                if not current_j-1 >= 0:
                    break
                current_j -= 1
            
        current_j = j+1
        if current_j < self.GameSettings.boardSideLength:
            while board[current_i][current_j] != self.GameSettings.blankSpaceSymbol:
                if board[current_i][current_j] == testStone:
                    numOfStonesConnected += 1
                else:
                    break
                if not current_j+1 < self.GameSettings.boardSideLength:
                    break
                current_j += 1
        return numOfStonesConnected
    
    # get the number of identical connected \ diagonal stones
    def __GetFirstDiagonalConnectedStones(self, board, testStone, i, j): 
        numOfStonesConnected = 0
    
        current_i = i+1
        current_j = j+1
        if current_i < self.GameSettings.boardSideLength and current_j < self.GameSettings.boardSideLength:
            while board[current_i][current_j] != self.GameSettings.blankSpaceSymbol:
                if board[current_i][current_j] == testStone:
                    numOfStonesConnected += 1
                else:
                    break
                if not (current_i+1 < self.GameSettings.boardSideLength and current_j+1 < self.GameSettings.boardSideLength):
                    break
                current_i += 1
                current_j += 1
            
        current_i = i-1
        current_j = j-1
        if current_i >= 0 and current_j >= 0:
            while board[current_i][current_j] != self.GameSettings.blankSpaceSymbol:
                if board[current_i][current_j] == testStone:
                    numOfStonesConnected += 1
                else:
                    break
                if not (current_i-1 >= 0 and current_j-1 >= 0):
                    break
                current_i -= 1
                current_j -= 1
        return numOfStonesConnected
    
    # get the number of identical connected / diagonal stones
    def __GetSecondDiagonalConnectedStones(self, board, testStone, i, j):
        numOfStonesConnected = 0
    
        current_i = i+1
        current_j = j-1
        if current_i < self.GameSettings.boardSideLength and current_j >= 0:
            while board[current_i][current_j] != self.GameSettings.blankSpaceSymbol:
                if board[current_i][current_j] == testStone:
                    numOfStonesConnected += 1
                else:
                    break
                if not (current_i+1 < self.GameSettings.boardSideLength and current_j-1 >= 0):
                    break
                current_i += 1
                current_j -= 1
            
        current_i = i-1
        current_j = j+1
        if current_i >= 0 and current_j < self.GameSettings.boardSideLength:
            while board[current_i][current_j] != self.GameSettings.blankSpaceSymbol:
                if board[current_i][current_j] == testStone:
                    numOfStonesConnected += 1
                else:
                    break
                if not (current_i-1 >= 0 and current_j+1 < self.GameSettings.boardSideLength):
                    break
                current_i -= 1
                current_j += 1
        return numOfStonesConnected
    
##########################################################################################################
##########################################################################################################
##########################################################################################################

# blueprint of a game object
class Game:
    def __init__(self, GameSettings):
        self.__GameSettings = GameSettings
        self.__board = self.__CreateNewBoard()
        self.__turn = 1
        self.__players = []
        
    ################ Getters ################
    def __GetterGameSettings(self):
        return self.__GameSettings
    def __GetterBoard(self):
        return self.__board
    def __GetterTurn(self):
        return self.__turn
    def __GetterPlayers(self):
        return self.__players
    
    ############### Setters ##################
    def __SetterTurn(self, value):
        self.__wins = value
    
    ################ Properties ###############
    GameSettings = property(fget=__GetterGameSettings)
    board = property(fget=__GetterBoard)
    turn = property(fget=__GetterTurn, fset=__SetterTurn)
    players = property(fget=__GetterPlayers)
    
    ########################### Game Progression ##########################
    #make a step in the game
    #it returns who won the game
    def Step(self, action):
        self.board[action[1]][action[0]] = self.turn
        self.players[self.turn-1].capturedPairs += self.__GetCapture(self.board, self.turn, action)
        playerWon = None
        if self.__IsGameEnd(self.board, self.turn, self.players[0].capturedPairs, self.players[1].capturedPairs):
            playerWon = self.turn
        if self.__IsBoardFull():
            playerWon = 3
        self.__ChangeTurn()
        return playerWon
    
    #simulate the game step with a give state and a given action
    def SimStep(self, state, action):
        #backup the current game state
        backupBoard = self.board
        backupTurn = self.turn
        backupCapturedPlayer1Pairs = self.players[0].capturedPairs
        backupCapturedPlayer2Pairs = self.players[1].capturedPairs
        
        #use and play from the give state
        self.board = state.board.copy()
        self.turn = state.turn
        self.players[0].capturedPairs = state.capturedPlayer1Pairs
        self.players[1].capturedPairs = state.capturedPlayer2Pairs
        playerWon = self.Step(action)
        newState = self.GetState()
        
        #restore the current game state
        self.board = backupBoard
        self.turn = backupTurn
        self.players[0].capturedPairs = backupCapturedPlayer1Pairs
        self.players[1].capturedPairs = backupCapturedPlayer2Pairs
        
        return newState, playerWon
    
    ########################### Board #################################
    #it creates a 2d square matrix of given side length, filled with given symbol
    #it returns the 2d matrix
    def __CreateNewBoard(self):
        return np.full((self.GameSettings.boardSideLength, self.GameSettings.boardSideLength), self.GameSettings.blankSpaceSymbol)

    #it outputs the game board to the user interface
    def PrintBoard(self):
        rowsIndex = []
        columnsIndex = []
        for idx in range(self.GameSettings.boardSideLength):
            if len(str(idx)) == 1:
                column = " " + str(idx) + " "
            if len(str(idx)) == 2:
                column = str(idx) + " "
            columnsIndex.append(column)
    
        for idx in range(self.GameSettings.boardSideLength):
            if len(str(idx)) == 1:
                row = str(idx) + "  "
            elif len(str(idx)) == 2:
                row = str(idx) + " "
            rowsIndex.append(row)
        print "    ",
        for x in range(len(columnsIndex)-1):
            print columnsIndex[x],
        print columnsIndex[-1]
        for j in range(self.GameSettings.boardSideLength):
            self.__PrintHorizontalLineRow()
            print rowsIndex[j],
            for i in range(self.GameSettings.boardSideLength):
                symbol = self.board[j][i]
                if symbol == 0:
                    symbol = " "
                self.__PrintVerticalLineRow(symbol)
            print "|"
        self.__PrintHorizontalLineRow()
        
    # print row with horizontal lines
    def __PrintHorizontalLineRow(self):
        print "     "+"--- " * self.GameSettings.boardSideLength
    
    # print row with vertical lines
    def __PrintVerticalLineRow(self, symbol):
        print "| "+ str(symbol),
        
    

    ######################## Checking Processes ############################
    
    # check if the board is full
    # it returns true of false
    def __IsBoardFull(self):
        for i in range(self.GameSettings.boardSideLength):
            for j in range(self.GameSettings.boardSideLength):
                if self.board[i][j] == self.GameSettings.blankSpaceSymbol:
                    return False
        return True
    
    # check if the action is valid
    # it returns true or false
    def __IsValidAction(self, action):
        try:
            if 0 <= action[0] <= self.GameSettings.boardSideLength and 0 <= action[1] <= self.GameSettings.boardSideLength:
                    return (self.board[action[1]][action[0]] == self.GameSettings.blankSpaceSymbol)
        except:
            return False
        return False
    
    # check if the current action is a capture move
    # it will update the board if true and count the number of pairs captured. 
    # it returns the total number of captured pairs
    def __GetCapture(self, board, currPlayerSymbol, action):
        if currPlayerSymbol == self.GameSettings.playerTwoStoneSymbol:
            notPlayerSymbol = self.GameSettings.playerOneStoneSymbol
        else:
            notPlayerSymbol = self.GameSettings.playerTwoStoneSymbol
            
        numCapturedPair = 0
        
        i = action[1]
        j = action[0]
    
        # check for vertical capture
        if (j > 2) and \
        (board[i][j-1] == notPlayerSymbol) and \
        (board[i][j-2] == notPlayerSymbol) and \
        (board[i][j-3] == currPlayerSymbol):
            board[i][j-1] = self.GameSettings.blankSpaceSymbol
            board[i][j-2] = self.GameSettings.blankSpaceSymbol
            numCapturedPair += 1
        
        if (j < self.GameSettings.boardSideLength-3) and \
        (board[i][j+1] == notPlayerSymbol) and \
        (board[i][j+2] == notPlayerSymbol) and \
        (board[i][j+3] == currPlayerSymbol):
            board[i][j+1] = self.GameSettings.blankSpaceSymbol
            board[i][j+2] = self.GameSettings.blankSpaceSymbol
            numCapturedPair += 1
        
        #check for horizontal capture
        if (i > 2) and \
        (board[i-1][j] == notPlayerSymbol) and \
        (board[i-2][j] == notPlayerSymbol) and \
        (board[i-3][j] == currPlayerSymbol):
            board[i-1][j] = self.GameSettings.blankSpaceSymbol
            board[i-2][j] = self.GameSettings.blankSpaceSymbol
            numCapturedPair += 1
        
        if (i < self.GameSettings.boardSideLength-3) and \
        (board[i+1][j] == notPlayerSymbol) and \
        (board[i+2][j] == notPlayerSymbol) and \
        (board[i+3][j] == currPlayerSymbol):
            board[i+1][j] = self.GameSettings.blankSpaceSymbol
            board[i+2][j] = self.GameSettings.blankSpaceSymbol
            numCapturedPair += 1

        #check for \ diagonal capture
        if (i > 2) and \
        (j > 2) and \
        (board[i-1][j-1] == notPlayerSymbol) and \
        (board[i-2][j-2] == notPlayerSymbol) and \
        (board[i-3][j-3] == currPlayerSymbol):
            board[i-1][j-1] = self.GameSettings.blankSpaceSymbol
            board[i-2][j-2] = self.GameSettings.blankSpaceSymbol
            numCapturedPair += 1
        
        if (i < self.GameSettings.boardSideLength-3) and \
        (j < self.GameSettings.boardSideLength-3) and \
        (board[i+1][j+1] == notPlayerSymbol) and \
        (board[i+2][j+2] == notPlayerSymbol) and \
        (board[i+3][j+3] == currPlayerSymbol):
            board[i+1][j+1] = self.GameSettings.blankSpaceSymbol
            board[i+2][j+2] = self.GameSettings.blankSpaceSymbol
            numCapturedPair += 1
        
        #check for / diagonal capture
        if (i > 2) and \
        (j < self.GameSettings.boardSideLength-3) and \
        (board[i-1][j+1] == notPlayerSymbol) and \
        (board[i-2][j+2] == notPlayerSymbol) and \
        (board[i-3][j+3] == currPlayerSymbol):
            board[i-1][j+1] = self.GameSettings.blankSpaceSymbol
            board[i-2][j+2] = self.GameSettings.blankSpaceSymbol
            numCapturedPair += 1
        
        if (i < self.GameSettings.boardSideLength-3) and \
        (j > 2) and \
        (board[i+1][j-1] == notPlayerSymbol) and \
        (board[i+2][j-2] == notPlayerSymbol) and \
        (board[i+3][j-3] == currPlayerSymbol):
            board[i+1][j-1] = self.GameSettings.blankSpaceSymbol
            board[i+2][j-2] = self.GameSettings.blankSpaceSymbol
            numCapturedPair += 1
            
        return numCapturedPair

    # check every position on the board to see if a win condition has been met
    # it returns true or false
    def __IsGameEnd(self, board, currPlayerSymbol, capturedPlayer1Pairs, capturedPlayer2Pairs):

        # check for horizontal win condition
        for j in range(self.GameSettings.boardSideLength):
            for i in range(self.GameSettings.boardSideLength-4):
                if (board[i][j] == currPlayerSymbol) and \
                   (board[i+1][j] == currPlayerSymbol) and \
                   (board[i+2][j] == currPlayerSymbol) and \
                   (board[i+3][j] == currPlayerSymbol) and \
                   (board[i+4][j] == currPlayerSymbol):
                    return True

        # check for vertical win condition
        for i in range(self.GameSettings.boardSideLength):
            for j in range(self.GameSettings.boardSideLength-4):
                if (board[i][j] == currPlayerSymbol) and \
                   (board[i][j+1] == currPlayerSymbol) and \
                   (board[i][j+2] == currPlayerSymbol) and \
                   (board[i][j+3] == currPlayerSymbol) and \
                   (board[i][j+4] == currPlayerSymbol):
                    return True

        # check for / diagonal win condition
        for i in range(self.GameSettings.boardSideLength-4):
            for j in range(4, self.GameSettings.boardSideLength):
                if (board[i][j] == currPlayerSymbol) and \
                   (board[i+1][j-1] == currPlayerSymbol) and \
                   (board[i+2][j-2] == currPlayerSymbol) and \
                   (board[i+3][j-3] == currPlayerSymbol) and \
                   (board[i+4][j-4] == currPlayerSymbol):
                    return True

        # check for \ diagonal win condition
        for i in range(self.GameSettings.boardSideLength-4):
            for j in range(self.GameSettings.boardSideLength-4):
                if (board[i][j] == currPlayerSymbol) and \
                   (board[i+1][j+1] == currPlayerSymbol) and \
                   (board[i+2][j+2] == currPlayerSymbol) and \
                   (board[i+3][j+3] == currPlayerSymbol) and \
                   (board[i+4][j+4] == currPlayerSymbol):
                    return True

        # check for win by captured pairs condition
        if currPlayerSymbol == self.GameSettings.playerOneStoneSymbol:
            if capturedPlayer2Pairs >= 5:
                return True
        else:
            if capturedPlayer1Pairs >= 5:
                return True
        return False
    
    ########################## Utilities #################################
    
    # initialise and return an game state object
    def GetState(self):
        state = GameState(self.board, self.turn, self.players[0].capturedPairs, self.players[1].capturedPairs, self.GameSettings)
        return state
    
    # display the current game state and last player's move
    def PrintLastPlayerAction(self, action):
        print
        print
        time.sleep(self.GameSettings.pauseTime)
        self.PrintBoard()
        time.sleep(self.GameSettings.pauseTime)
        print 'Player ' + str(self.board[action[1]][action[0]]) + ' Placed Stone At ==> ',
        print 'Column ' + str(action[0]),
        print 'Row ' + str(action[1])
        time.sleep(self.GameSettings.pauseTime)
        print 'Captured Player 1 ==> ' + str(self.players[0].capturedPairs)
        time.sleep(self.GameSettings.pauseTime)
        print 'Captured Player 2 ==> ' + str(self.players[1].capturedPairs)
        time.sleep(self.GameSettings.pauseTime)
        print 'Player ' + str(self.turn) + "'s Turn"
    
    # display the first player's turn message
    def InitialiseGame(self):
        print
        self.PrintBoard()
        time.sleep(self.GameSettings.pauseTime)
        print 'Player ' + str(self.turn) + "'s Turn"
        time.sleep(self.GameSettings.pauseTime)
        print 'Player ' + str(self.turn) + ' Automatic First Move'
        time.sleep(self.GameSettings.pauseTime)
        action, playerWon = self.__SetRootState()
        return action, playerWon
    
    # place the first player's stone at the center of the board
    def __SetRootState(self):
        action = [((self.GameSettings.boardSideLength-1)/2), ((self.GameSettings.boardSideLength-1)/2)]
        playerWon = self.Step(action)
        return action, playerWon
    
    # randomly decide first move
    def GetRandomFirstTurn(self):
        if random.randint(0, 1) == 1:
            return 1
        else:
            return 2
    
    # change turns
    def __ChangeTurn(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1
    
    # get the next player action
    def GetPlayerAction(self, node):
        action = self.players[self.turn-1].GetAction(node)
        while not self.__IsValidAction(action):
            print 'Please choose an empty space on the board.'
            action = self.players[self.turn-1].GetAction(node)
        return action
    
    
    
    
    
    
