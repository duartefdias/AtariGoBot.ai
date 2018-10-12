import game

myGame = game.Game()

# Open file stream for saving game state
f = open('board', 'r')

# Get board state from file
state = myGame.load_board(f)

print(state)