import go
from alphabeta_cutoff_search import alphabeta_cutoff_search

def mainAiAi():
    s = []
    endGame = 0

    myGame = go.Game()
    s = myGame.load_board(open('boards/emptyBoard.txt', 'r'))

    while not endGame:
        # Print board
        myGame.print_board(s)
        print("Player 1's utility (X): " + str(myGame.utility(s, 1)))
        print("Player 2's utility (O): " + str(myGame.utility(s, 2)))
        print("Player 1's actions: " + str(myGame.actions(s)))

        # AI 1's turn
        AiMove = alphabeta_cutoff_search(s, myGame, d=3)
        if AiMove:
            s = myGame.result(s, AiMove)
        endGame = myGame.terminal_test(s)

        if endGame:
            break

        myGame.print_board(s)
        print("Player 1's utility (X): " + str(myGame.utility(s, 1)))
        print("Player 2's utility (O): " + str(myGame.utility(s, 2)))
        print("Player 1's actions: " + str(myGame.actions(s)))

        # AI 2's turn
        AiMove = alphabeta_cutoff_search(s, myGame, d=3)
        if AiMove:
            s = myGame.result(s, AiMove)
        endGame = myGame.terminal_test(s)

    # Print the final board
    myGame.print_board(s)
    print("Player 1's utility (X): " + str(myGame.utility(s, 1)))
    print("Player 2's utility (O): " + str(myGame.utility(s, 2)))
    print("Player 1's actions: " + str(myGame.actions(s)))

mainAiAi()