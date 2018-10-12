import game

myGame = game.Game()

# Open file stream for saving game state
f = open('board', 'r')

# Get board state from file
state = myGame.load_board(f)

print(state)

# Print board
print(str(state[0]) + ' ' + str(state[1]))
for i in range(2, state[0] + 2):
    if (i - 2) % state[0] == 0:
        print('\n')
    print(str(state[i]))