from game import Game
import group

s = []
endGame = 0
playerMove = 0

s = Game.load_board(open('board', 'r'))
myGame = Game(s)
print(s)

# Group pieces in initial board configuration
for piecePos in range(0, len(s[2:])):
    print(piecePos)
    if s[piecePos + 2] != 0:
        # Specify to which player the piece belongs to
        s[1] = s[piecePos + 2]
        # Create a group for new piece
        newPiece = group.Group(myGame, s, piecePos)
        # Podemos correr isto passo a passo no debug? SURE
        s[piecePos + 2] = newPiece.id
        # Join new group to other groups
        s = newPiece.search_nearby_groups(s, myGame, piecePos)

# Set next player to human
s[1] = 1

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

    print(s)

    # Player's turn
    while playerMove == 0:
        playerInputX = input("It's your turn! (choose a tile number or 'x' to show possible plays)\nX: ")
        if playerInputX == 'x' or playerInputX == 'X':
            print(myGame.actions(s))
        else:
            playerInputY = input("Y: ")
            playerInput = [int(playerInputX), int(playerInputY)]
            for possibleAction in myGame.actions(s):
                if playerInput == possibleAction:
                    playerMove = playerInput
                    break
            if playerMove == 0:
                print('Invalid move! Try again!')
                
    playerMove.insert(0, 1) # Insert player id in beginning of list
    s = myGame.result(s, playerMove)

    # Convert coordinates to single number 
    piecePos = ((int(playerInputX))*myGame.boardSize) +  int(playerInputY)
    print('Player input: ' + str(piecePos))
    newPiece = group.Group(myGame, s, piecePos)
    s[piecePos + 2] = newPiece.id

    # Search groups nearby the new piece
    s = newPiece.search_nearby_groups(s, myGame, piecePos)
    playerMove = 0

    # End of human's turn
    # Set next player to AI
    s[1] = 2

    # AI's turn
    # MAGIC AI code


    # End of AI's turn
    # Set next player to human
    s[1] = 1