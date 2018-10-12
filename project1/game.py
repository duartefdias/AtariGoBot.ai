'''
state = < n, p, x0, x1, ..., x(n-1) >

n = board size (example: n=4 corresponds to a 4x4 board)
p = next player to move (p=1 or p=2)

'''

class Game:
    """Atari Go game engine"""
    
    def ___init___(self):
        f = open('board', 'r')
        boardFile = self.load_board(f)
        self.boardSize = boardFile[0]
        self.nextPlayer = boardFile[1]
        self.groups = self.get_groups(boardFile[2:])
        self.state = []
        self.state[0] = self.get_player_score(1)
        self.state[1] = self.get_player_score(2)

    def to_move(self, s):
        # Returns the player to move next given the state s
        return s[1]
    '''
    def terminal_test(self, s):
        # Returns a boolean of whether the state s is terminal

    def utility(self, s, p):
        # Returns 1 if pwins, -1 if p loses, 0 in case of a draw

    def actions(self, s):
        # Returns a list of valid moves at state s

    def result(self, s, a):
        # Returns the sucessor game state after playing move a at state s
    '''
    def load_board(self, s):
        # Loads a board from an opened file stream s and returns the corresponding state
        rawState = s.readlines()

        # Parse data
        state = []
        state.append(int(rawState[0][0]))
        state.append(int(rawState[0][2]))

        for i in range(1, state[0] + 1):
            for j in range(0, state[0]):
                state.append(int(rawState[i][j])) 
        
        return state

    def get_player_score(self, player):
        # Returns player's group of pieces with lowest degrees of freedom
        # 1 -> player 1, 2 -> player 2
        return 1

    def get_groups(self, boardState):
        return []

    