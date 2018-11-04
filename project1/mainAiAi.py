import go
from alphabeta_cutoff_search import alphabeta_cutoff_search
#import pstatsviewer

def mainAiAi():
    s = []
    endGame = 0

    myGame = go.Game()
    s = myGame.load_board(open('boards/test5_3.txt', 'r'))

    while not endGame:
        # Print board
        myGame.print_board(s)
        print("Player 1's utility (X): " + str(myGame.utility(s, 1)))
        print("Player 2's utility (O): " + str(myGame.utility(s, 2)))

        # AI 1's turn
        AiMove = alphabeta_cutoff_search(s, myGame, d=5)
        if AiMove:
            s = myGame.result(s, AiMove)
        endGame = myGame.terminal_test(s)

        myGame.print_board(s)
        print("Player 1's utility (X): " + str(myGame.utility(s, 1)))
        print("Player 2's utility (O): " + str(myGame.utility(s, 2)))

        # AI 2's turn
        AiMove = alphabeta_cutoff_search(s, myGame, d=5)
        if AiMove:
            s = myGame.result(s, AiMove)
        endGame = myGame.terminal_test(s)

    # Print the final board
    myGame.print_board(s)

mainAiAi()