from game import Game
import group
import alphabeta_cutoff_search

s = []
endGame = 0

s = Game.load_board(open('project1/boards/assignment_example.txt', 'r'))
myGame = Game(s)
print(s)

# Group pieces in initial board configuration
s = myGame.get_groups(s)

# Set next player to human
s[1] = 1

while not endGame:
    # Set playerMove to 0, indicating that the player hasn't yet chosen a valid move
    playerMove = 0

    # Print board
    print('\n')
    for i in range(2, len(s)):
        if s[i] == 0:
            print(' _ ', end="")
        if s[i] % 2 == 1:
            print(' X ', end="")
        if s[i] % 2 == 0 and s[i] != 0:
            print(' O ', end="")
        if ((i-1) % myGame.boardSize) == 0:
            print('\n')

    print(s)

    # Player's turn
    while playerMove == 0:
        playerInputX = input("It's your turn! (choose a tile number or type 'help' to show possible plays)\nX: ")
        if playerInputX == 'help' or playerInputX == 'Help':
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
                
    # Insert player id in beginning of list
    # playerMove.insert(0, 1)
    # André: There's no need for this I think
    
    # s = myGame.result(s, playerMove)

    # End of human's turn
    # Set next player to AI
    s[1] = 2

    # AI's turn
    # MAGIC AI code
    
    # Get the AI to decise what's the best move
    AiMove = alphabeta_cutoff_search.alphabeta_cutoff_search(s, myGame, d=4)
    s = myGame.result(s, AiMove)

    # [Debug] Code to debug the max score possible in the current board
    # boardSize = int(input("Choose a board size: "))
    # max_score = Game.board_max_score(boardSize)
    # print("The maximum possible score for a board of size " + str(boardSize) + " is " + str(max_score))

    # End of AI's turn
    # Set next player to human
    s[1] = 1

    endGame = myGame.terminal_test(s)