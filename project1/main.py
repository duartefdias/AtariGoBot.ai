import game
import group

s = []
endGame = 0
playerMove = 0

myGame = game.Game()
s = myGame.load_board(open('board', 'r'))
print(s)

while not endGame:

    # Print board
    print('\n')
    for i in range(2, len(s)):
        if s[i] == 0:
            print(' _ ', end="")
        if s[i] % 2 == 1 and s[i] != 0:
            print(' X ', end="")
        if s[i] % 2 == 0 and s[i] != 0:
            print(' O ', end="")
        if ((i-1) % s[0]) == 0:
            print('\n')

    # Player's turn
    while playerMove == 0:
        playerInput = input("It's your turn! (choose a tile number or 'x' to show possible plays):\n")
        if playerInput == 'x' or playerInput == 'X':
            print(myGame.actions(s))
        else:
            for possibleAction in myGame.actions(s):
                if int(playerInput) == possibleAction:
                    playerMove = playerInput
                    break
            if playerMove == 0:
                print('Invalid move! Try again!')

    s = group.Group(myGame, s, 'something')
    playerMove = 0

    # AI's turn
    # MAGIC AI code