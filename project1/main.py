from .game import Game
from .group import Group

s = []
endGame = 1
playerMove = 0

myGame = game.Game()
myGame.load_board(myGame)
print(myGame.state)

while not endGame:

    # Print board
    for i in range(2, len(myGame.state)):
        if myGame.state[i] == 0:
            print(' _ ')
        if myGame.state[i] % 2 == 1:
            print(' X ')
        if myGame.state[i] % 2 == 0:
            print(' O ')
        if i-1 % myGame.state[0] == 0:
            print('\n')

    # Player's turn
    while playerMove == 0:
        playerInput = input("It's your turn! (choose a tile number or 'x' to show possible plays):\n")
        if playerInput == 'x' or playerInput == 'X':
            print(myGame.actions(s))
        else:
            for possibleAction in myGame.actions(s):
                if playerInput == possibleAction:
                    playerMove = playerInput
            if playerMove == 0:
                print('Invalid move! Try again!')

    newPiece = group.Group()
    playerMove = 0

    # AI's turn