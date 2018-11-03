import go
from alphabeta_cutoff_search import alphabeta_cutoff_search

s = []
endGame = 0

myGame = go.Game()
s = myGame.load_board(open('boards/test3_1.txt', 'r'))

while not endGame:
    # Print board
    # myGame.print_board(s)

    # AI 1's turn
    AiMove = alphabeta_cutoff_search(s, myGame, d=10)
    s = myGame.result(s, AiMove)
    endGame = myGame.terminal_test(s)

    # AI 2's turn
    AiMove = alphabeta_cutoff_search(s, myGame, d=10)
    s = myGame.result(s, AiMove)
    endGame = myGame.terminal_test(s)

# Print the final board
# myGame.print_board(s)