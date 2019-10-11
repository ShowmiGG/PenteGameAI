# external libraries
from math import sqrt

################### Game Settings #####################
class GameSettings:
    def __init__(self):
        self.boardSideLength = 9 # the game board side length
        self.playerOneStoneSymbol = 1 # the player 1 symbol
        self.playerTwoStoneSymbol = 2 # the player 2 symbol
        self.blankSpaceSymbol = 0 # the blank symbol
        self.gameMode = '' # the current game mode
        self.pauseTime = 0.3 # the pause time during the game play process
        self.C = sqrt(2) # the exploration constant
        self.expansionNum = 1 # number of expansion
        self.playoutNum = 5 # the number of UCT playouts
        self.simulationNum = 20000 # the number of simulation playouts
        
        
#################### Headings and UI element displays ###################
PENTE = '''


               

                   
             _______                         __               
            /       \                       /  |              
            $$$$$$$  |  ______   _______   _$$ |_     ______  
            $$ |__$$ | /      \ /       \ / $$   |   /      \ 
            $$    $$/ /$$$$$$  |$$$$$$$  |$$$$$$/   /$$$$$$  |
            $$$$$$$/  $$    $$ |$$ |  $$ |  $$ | __ $$    $$ |
            $$ |      $$$$$$$$/ $$ |  $$ |  $$ |/  |$$$$$$$$/ 
            $$ |      $$       |$$ |  $$ |  $$  $$/ $$       |
            $$/        $$$$$$$/ $$/   $$/    $$$$/   $$$$$$$/ 
            
                




'''
PAUSE = '''
___  ____ _  _ ____ ____ 
|__] |__| |  | [__  |___ 
|    |  | |__| ___] |___ 
'''
MAIN_MENU = '''
_  _ ____ _ _  _    _  _ ____ _  _ _  _  
|\/| |__| | |\ |    |\/| |___ |\ | |  |
|  | |  | | | \|    |  | |___ | \| |__|
'''
PVP = '''
___  _    ____ _   _ ____ ____    _  _ ____    ___  _    ____ _   _ ____ ____ 
|__] |    |__|  \_/  |___ |__/    |  | [__     |__] |    |__|  \_/  |___ |__/ 
|    |___ |  |   |   |___ |  \     \/  ___]    |    |___ |  |   |   |___ |  \ 
'''
PVE = '''
___  _    ____ _   _ ____ ____    _  _ ____    ____ ____ _  _ ___  _  _ ___ ____ ____ 
|__] |    |__|  \_/  |___ |__/    |  | [__     |    |  | |\/| |__] |  |  |  |___ |__/ 
|    |___ |  |   |   |___ |  \     \/  ___]    |___ |__| |  | |    |__|  |  |___ |  \ 
'''
INSTRUCTIONS = '''
_ _  _ ____ ___ ____ _  _ ____ ___ _ ____ _  _ ____ 
| |\ | [__   |  |__/ |  | |     |  | |  | |\ | [__  
| | \| ___]  |  |  \ |__| |___  |  | |__| | \| ___] 
'''
SETTINGS = '''
____ ____ ___ ___ _ _  _ ____ ____ 
[__  |___  |   |  | |\ | | __ [__  
___] |___  |   |  | | \| |__] ___] 
'''
PLAYER_1_WON = '''
______ _                         _____                                  
| ___ \ |                       |  _  |                                 
| |_/ / | __ _ _   _  ___ _ __  | | | |_ __   ___  __      _____  _ __  
|  __/| |/ _` | | | |/ _ \ '__| | | | | '_ \ / _ \ \ \ /\ / / _ \| '_ \ 
| |   | | (_| | |_| |  __/ |    \ \_/ / | | |  __/  \ V  V / (_) | | | |
\_|   |_|\__,_|\__, |\___|_|     \___/|_| |_|\___|   \_/\_/ \___/|_| |_|
                __/ |                                                   
               |___/                                                    
'''
PLAYER_2_WON = '''
______ _                         _____                                   
| ___ \ |                       |_   _|                                  
| |_/ / | __ _ _   _  ___ _ __    | |_      _____   __      _____  _ __  
|  __/| |/ _` | | | |/ _ \ '__|   | \ \ /\ / / _ \  \ \ /\ / / _ \| '_ \ 
| |   | | (_| | |_| |  __/ |      | |\ V  V / (_) |  \ V  V / (_) | | | |
\_|   |_|\__,_|\__, |\___|_|      \_/ \_/\_/ \___/    \_/\_/ \___/|_| |_|
                __/ |                                                    
               |___/                                                     
'''
TIE = '''
 _____ _____ _____ 
|_   _|_   _|  ___|
  | |   | | | |__  
  | |   | | |  __| 
  | |  _| |_| |___ 
  \_/  \___/\____/ 
           
           
'''
USERINPUT = "==>"
GameManual = '''
Game Manual

 - Aim
   ...
 
 - Game rules
   ...
 
 - How to capture
   ...

'''

UIManual = '''
User Manual

 - How to play
   ...

 - How to change settings
   ...
 
 - How to 
   ...


'''

















