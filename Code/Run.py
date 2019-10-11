# external libraries
import time

# user defined modules
import Environment as gamePackage
import Agent as agentPackage
import UCT as uctPackage
import Config as cfg


def main():
    run = RunGame()
    run.MainMenu()

class RunGame:
    def __init__(self):
        self.__GameSettings = cfg.GameSettings()
        
    ################ Getters ################
    def __GetterGameSettings(self):
        return self.__GameSettings
    
    ################ Properties ###############
    GameSettings = property(fget=__GetterGameSettings)
    
    #################### Main Menu ###################
    def MainMenu(self):
        while True:
#            try:
            print cfg.PENTE
            print cfg.MAIN_MENU
            print "Options"
            print "1 - Player vs Player"
            print "2 - Player vs Computer"
            print "3 - Instruction"
            print "4 - Settings"
            print "x - Quit"
            option = str(raw_input(cfg.USERINPUT)).lower()
            self.__InputResponse(option)
            if option == '1':
                self.__PlayPlayerVsPlayerGame()
            elif option == '2':
                self.__SetGameMode()
                self.__PlayUCTGame()
            elif option == '3':
                self.__InstructionsMenu()
            elif option == '4':
                self.__SettingsMenu()
            elif option.lower() == 'x':
                print "Exiting..."
                time.sleep(1)
                print "Goodbye, Human."
                time.sleep(1)
                break
            else:
                print 'Please enter a valid option'
    #        except:
    #            print 'Please enter a valid option'
        exit()
            

    ############### Player vs Player ####################
    # start a player vs player game
    def __PlayPlayerVsPlayerGame(self):
        self.GameSettings.gameType = "PVP"
        print cfg.PVP
        game = gamePackage.Game(self.GameSettings)
        player1 = agentPackage.Human("Player 1")
        player2 = agentPackage.Human("Player 2")
        game.players = [player1, player2]
        self.__PrintGameDescription("Human","Human")
        game.turn = self.__GetFirstPlayer(game)
        self.__StartGameCountDown()
        action, playerWon = game.InitialiseGame()
        while True:
            game.PrintLastPlayerAction(action)
            action = game.GetPlayerAction(node=None)
            playerWon = game.Step(action)
            if playerWon != None:
                self.__PrintEndGameDisplay(game, playerWon)
                break
        
    ############### Player vs Computer ####################
    # start a player vs computer game that uses a UCT algorithm to select moves
    def __PlayUCTGame(self):
        self.GameSettings.gameType = "UCT"
        print cfg.PVE
        game = gamePackage.Game(self.GameSettings)
        player1 = agentPackage.Human("Player 1")
        player2 = agentPackage.Agent("Player 2", game)
        game.players = [player1, player2]
        self.__PrintGameDescription("Human", "Computer")
        game.turn = self.__GetFirstPlayer(game)
        self.__StartGameCountDown()
        action, playerWon = game.InitialiseGame()
        game.players[game.turn-1].steps += 1
        while True:
            game.PrintLastPlayerAction(action)
            state = game.GetState()
            node = uctPackage.Node(state, playerWon)
            action = game.GetPlayerAction(node)
            playerWon = game.Step(action)
            game.players[game.turn-1].steps += 1
            if playerWon != None:
                self.__PrintEndGameDisplay(game, playerWon)
                break
    
    ############### Settings ####################
    # display the current settings and allows the user to change the settings
    def __SettingsMenu(self):
        while True:
            try:
                print cfg.SETTINGS
                print "Current Setting"
                print "Board size ==>", self.GameSettings.boardSideLength
                print "Exploration constant C ==>", self.GameSettings.C
                print "UCT playout number ==>", self.GameSettings.playoutNum
                print
                print "Options"
                print "1 - Change board size"
                print "2 - Change exploration constant C"
                print "3 - Change UCT playout number"
                print "x - Back to main menu"
                option = str(raw_input(cfg.USERINPUT)).lower()
                self.__InputResponse(option)
                options = ['1', '2', '3', 'x']
                if option in options:
                    break
                else:
                    print 'Please enter a valid option'
            except:
                print 'Please enter a valid option'
        if option == '1':
            self.GameSettings.boardSideLength = self.__ChangeBoardSize()
        elif option == '2':
            self.GameSettings.C = self.__ChangeC()
        elif option == '3':
            self.GameSettings.playoutNum = self.__ChangePlayoutNum()

    #allow user to change the size of the board
    def __ChangeBoardSize(self):
        while True:
            try:
                print
                print "Enter new board size (between 5<x<19 and odd)"
                newSideLen = str(raw_input(cfg.USERINPUT)).lower()
                self.__InputResponse(newSideLen)
                newSideLen = int(newSideLen)
                if  newSideLen > 4 and newSideLen < 20 and (newSideLen % 2) != 0:
                    print "Board size changed to ==>", newSideLen
                    return newSideLen
                else:
                    print 'Please enter a valid option'
            except:
                print 'Please enter a valid option'
    
    #allows user to change the exploration constant c
    def __ChangeC(self):
        while True:
            try:
                print
                print "Enter new exploration constant C"
                newC = str(raw_input(cfg.USERINPUT)).lower()
                self.__InputResponse(newC)
                newC = int(newC)
                print "Exploration constant C change to ==>", newC
                return newC
            except:
                print 'Please enter a valid option'

    #allows user to change the number of UCT playouts
    def __ChangePlayoutNum(self):
        while True:
            try:
                print
                print "Enter new UCT playout number"
                newPlayoutNum = str(raw_input(cfg.USERINPUT)).lower()
                self.__InputResponse(newPlayoutNum)
                newPlayoutNum = int(newPlayoutNum)
                print "UCT playout number change to ==>", newPlayoutNum
                return newPlayoutNum
            except:
                print 'Please enter a valid option'


    ############### Instructions #####################
    #display the instructions menu and allow the user to choose the manual to read
    def __InstructionsMenu(self):    
        while True:
            try:
                print cfg.INSTRUCTIONS
                print "1 - Game manual"
                print "2 - User interface manual"
                print "x - Back to main menu"
                
                option = str(raw_input(cfg.USERINPUT)).lower()
                self.__InputResponse(option)
                options = ['1', '2', 'x']
                if option in options:
                    break
                else:
                    print 'Please enter a valid option'
            except: 
                print 'Please enter a valid option'
        if option == '1':
            print cfg.GameManual
        elif option == '2':
            print cfg.UIManual
        elif option == 'x':
            self.MainMenu()
    

    
    ############### Utilities ##################### 
    # display the essential game information
    def __PrintGameDescription(self, player1, player2):
        print
        print "Player 1 ==> ",
        time.sleep(self.GameSettings.pauseTime)
        print player1
        time.sleep(self.GameSettings.pauseTime)
        print "Player 2 ==> ",
        time.sleep(self.GameSettings.pauseTime)
        print player2
        time.sleep(self.GameSettings.pauseTime)
        print 
        print "Player 1 Stone Symbol ==> ",
        time.sleep(self.GameSettings.pauseTime)
        print self.GameSettings.playerOneStoneSymbol
        time.sleep(self.GameSettings.pauseTime)
        print "Player 2 Stone Symbol ==> ",
        time.sleep(self.GameSettings.pauseTime)
        print self.GameSettings.playerTwoStoneSymbol
        time.sleep(self.GameSettings.pauseTime)
    
    # display the countdown to the start of the game
    def __StartGameCountDown(self):
        time.sleep(self.GameSettings.pauseTime)
        print "Creating game..."
        time.sleep(self.GameSettings.pauseTime)
        print "Game starting in...",
        time.sleep(self.GameSettings.pauseTime)
        print "3",
        time.sleep(1)
        print "2",
        time.sleep(1)
        print "1"
        time.sleep(1)

    # display how the user input is read by the computer
    def __InputResponse(self, userInput):
        print 'You have inputted - ', userInput
        print
    
    # allows the user to choose who goes first
    def __GetFirstPlayer(self, game):
        while True:
            try:
                print('''
Who plays first?
1 - Player 1
2 - Player 2
3 - Random
''')
                option = str(raw_input(cfg.USERINPUT)).lower()
                self.__InputResponse(option)
                options = ['1', '2', '3']
                if option in options:
                    break
                else:
                    print 'Please enter a valid option'
            except:
                print 'Please enter a valid option'
        if option == '1' or option == '2':
            return int(option)
        elif option == '3':
            return game.GetRandomFirstTurn()
          
    # allows the user to choose the difficulty level
    def __SetGameMode(self):
        while True:
            try:
                print('''
What AI you want to play aginst?
1 - Easy
2 - Normal
3 - Hard
''')
                option = str(raw_input(cfg.USERINPUT)).lower()
                self.__InputResponse(option)
                options = ['1', '2', '3']
                if option in options:
                    break
                else:
                    print 'Please enter a valid option'
            except:
                print 'Please enter a valid option'
                
        if option == '1':
            self.GameSettings.mode = 'Easy'
        elif option == '2':
            self.GameSettings.mode = 'Normal'
        elif option == '3':
            self.GameSettings.mode = 'Hard'
            
    # display the end of game screen when a game has ended
    def __PrintEndGameDisplay(self, game, playerWon):
        time.sleep(self.GameSettings.pauseTime)
        if playerWon == 1:
            print cfg.PLAYER_1_WON
        elif playerWon == 2:
            print cfg.PLAYER_2_WON
        elif playerWon == 3:
            print cfg.TIE
        time.sleep(self.GameSettings.pauseTime)
        game.PrintBoard()
        time.sleep(self.GameSettings.pauseTime)
        print "Captured Player 1 ==> " + str(game.players[0].capturedPairs)
        time.sleep(self.GameSettings.pauseTime)
        print "Captured Player 2 ==> " + str(game.players[1].capturedPairs)
        time.sleep(self.GameSettings.pauseTime)
        print "Player 1 Number of Steps ==>" + str(game.players[0].steps)
        time.sleep(self.GameSettings.pauseTime)
        print "Player 2 Number of Steps ==>" + str(game.players[1].steps)
        time.sleep(self.GameSettings.pauseTime)

#initiate the program
if __name__ == "__main__":
    main()
    
