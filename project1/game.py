'''
state = < n, p, x0, x1, ..., x(n-1) >

n = board size (example: n=4 corresponds to a 4x4 board)
p = next player to move (p=1 or p=2)

'''

import group

class Game:
    """Atari Go game engine"""
    
    def ___init___(self, s):
        f = open('board', 'r')
        s = self.load_board(f)
        self.boardSize = s[0]
        self.nextPlayer = s[1]
        self.groups = self.get_groups(s[2:])

        # List of available id's for player groups
        # First row: player one's available group ids
        # Second row: player two's available group ids
        self.freeIds = [[]]

    def to_move(self, s):
        # Returns the player to move next given the state s
        return s[1]
    
    def terminal_test(self, s):
        # Returns a boolean of whether the state s is terminal

        # Tests if game ends because DOF = 0 of either players
        for group in self.groups:
            if(group.dof == 0):
                return True

        # Tests if there are no more possible actions (draw)
        if(self.actions(s) == []):
            return True

        # Not terminal
        return False

    def utility(self, s, p):
        # Returns 1 if pwins, -1 if p looses, 0 in case of a draw
        # Else returns the score WRT a player

        minDofPlayerOne, minDofPlayerTwo  = 10000, 10000
        i, j = 0, 0

        # Search in game for min DOF and sums DOFs of groups for both players
        for group in self.groups:
            if(group.player == 1):
                if(group.dof < minDofPlayerOne):
                    minDofPlayerOne = group.dof

                    # Checking if game has ended at this point
                    if(minDofPlayerOne == 0 & p == 0):
                        return -1
                    if(minDofPlayerOne == 0 & p == 1):
                        return 1

                sumOne += group.dof
                i += 1 # counting the number of DOF's summed

            if(group.player == 2):
                if(group.dof < minDofPlayerTwo):
                    minDofPlayerTwo = group.dof

                    # Checking if game has ended at this point
                    if(minDofPlayerTwo == 0 & p == 0):
                        return 1
                    if(minDofPlayerTwo == 0 & p == 1):
                        return -1
                    
                sumTwo += group.dof  
                j += 1 # counting the number of DOF's summed         
     
        # Getting the average DOF of both players
        avgDofPlayerOne = sumOne/i
        avgDofPlayerTwo = sumTwo/j
            
        # Applying heuristic to both players (weights TBD)
        # IMPORTANT: MAKE SURE SCORE DOESNT EXCEED 1 ?HOW?
        weightMinPlayerOne = 0.5
        weightAvgPlayerOne = 0.5

        weightMinPlayerTwo = 0.5
        weightAvgPlayerTwo = 0.5

        scorePlayerOne = weightMinPlayerOne*minDofPlayerOne + weightAvgPlayerOne*avgDofPlayerOne
        scorePlayerTwo = weightMinPlayerTwo*minDofPlayerTwo + weightAvgPlayerTwo*avgDofPlayerTwo

        # Determining the score WRT a player
        score = scorePlayerOne-scorePlayerTwo
        
        if(p == 1):
            return score
        else:
            return -score


    def actions(self, s):
        # Returns a list of valid moves at state s
        possiblePlays = []
        for i in range(2, len(s)):
            if(s[i] == 0):
                i = s[i] % self.boardSize
                j = (s[i]-(i+1)) / self.boardSize
                possiblePlays.append([i, j])
        return possiblePlays

    def result(self, s, a):
        # Returns the sucessor game state after playing move a at state s
        # a is tuple {p, i, j} where p={1,2} is the player, i=1...n is the row and j=1...n is the column
        newState = s
        piecePos = a[1] + ((a[2]-1)*self.boardSize) #convert [i,j] into xs
        newGroup = group.Group(self, s, piecePos)
        newState = newGroup.search_nearby_groups(s, self, piecePos)
        if newState[1] == 1:
            newState[1] = 2
        elif newState[1] == 2:
            newState[1] = 1
        return newState

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

    def get_groups(self, s):
        return []

    # Gets a position's content from the board
    # Board example:
    # 1 2 3
    # 4 5 6
    # 7 8 9
    def get_board_space(self, s, spaceId):
        return s[spaceId + 1]

    # Set a position's content in the board
    # Board example:
    # 1 2 3
    # 4 5 6
    # 7 8 9
    def set_board_space(self, s, spaceId, value):
        s[spaceId + 1] = value
        return s                

    def find_groups(self, s, newPiece):
        return 1

    def order_moves(self, s, a)
        # Orders list of moves to place best in the beggining and speed up search
        return 1