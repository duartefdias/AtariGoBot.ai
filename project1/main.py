import go
from alphabeta_cutoff_search import alphabeta_cutoff_search

s = []
endGame = 0

myGame = go.Game()
s = myGame.load_board(open('boards/test4_1.txt', 'r'))

while not endGame:
    # Set playerMove to 0, indicating that the player hasn't yet chosen a valid move
    playerMove = 0

    # Print board
    myGame.print_board(s)

    # Player's turn
    while playerMove == 0:
        playerInputY = 'x'
        playerInputX = input("It's your turn! (choose a tile number or type 'help' to show possible plays)\nX: ")
        if playerInputX == 'help' or playerInputX == 'Help':
            print(myGame.actions(s))
        elif not playerInputX.isdigit():
            playerMove = 0
        else:
            while not playerInputY.isdigit():
                playerInputY = input("Y: ")
            playerInput = (s[1], int(playerInputX), int(playerInputY))
            playerMove = playerInput # Debug test 3.3
            # for possibleAction in myGame.actions(s):
            #     if playerInput == possibleAction:
            #         playerMove = playerInput
            #         break
            # if playerMove == 0:
            #     print('Invalid move! Try again!')
    
    s = myGame.result(s, playerMove)

    # Print board
    myGame.print_board(s)

    endGame = myGame.terminal_test(s)

    # Debug test 3.3
    print("Player 1's utility: " + str(myGame.utility(s, 1)))
    print("Player 2's utility: " + str(myGame.utility(s, 2)))
    
    if endGame:
        break

    # End of human's turn
    # Set next player to AI
    # s[1] = 2

    # AI's turn
    # MAGIC AI code
    
    # Get the AI to decise what's the best move
    AiMove = alphabeta_cutoff_search(s, myGame, d=10)
    s = myGame.result(s, AiMove)

    # [Debug] Code to debug the max score possible in the current board
    # boardSize = int(input("Choose a board size: "))
    # max_score = Game.board_max_score(boardSize)
    # print("The maximum possible score for a board of size " + str(boardSize) + " is " + str(max_score))

    # End of AI's turn
    # Set next player to human
    # s[1] = 1

    endGame = myGame.terminal_test(s)

# Print the final board
myGame.print_board(s)