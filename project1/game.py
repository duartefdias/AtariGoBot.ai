class Game:
    """Atari Go game engine"""

    def ___init___(self):
        #constructor code
    
    def to_move(self, s):
        # Returns the player to move next given the state s

    def terminal_test(self, s):
        # Returns a boolean of whether the state s is terminal

    def utility(self, s, p):
        # Returns 1 if pwins, -1 if p loses, 0 in case of a draw

    def actions(self, s):
        # Returns a list of valid moves at state s

    def result(self, s, a):
        # Returns the sucessor game state after playing move a at state s

    def load_board(self, s):
        # Loads a board from an opened file stream s and returns the corresponding state
        
