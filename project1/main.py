import game

myGame = game.Game()

print(state)

# Print board
print(str(state[0]) + ' ' + str(state[1]))
for i in range(2, state[0] + 2):
    if (i - 2) % state[0] == 0:
        print('\n')
    print(str(state[i]))