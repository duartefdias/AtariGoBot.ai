'''
state = < n, p, x0, x1, ..., x(n-1) >

n = board size (example: n=4 corresponds to a 4x4 board)
p = next player to move (p=1 or p=2)

'''

import group
import copy

class Game:
    """Atari Go game engine"""
    
    def __init__(self, s):
        self.boardSize = s[0]

        # List of available id's for player groups
        # First row: player one's available group ids
        # Second row: player two's available group ids
        self.freeIds = [[3], [4]]

        # Initialize the groups list as empty
        self.groups = []

    def to_move(self, s):
        # Returns the player to move next given the state s
        return s[1]
    
    def terminal_test(self, s):
        # Returns a boolean of whether the state s is terminal

        # The position of the game variable in the state
        game_pos_in_state = 2 + self.boardSize * self.boardSize

        # Tests if game ends because DOF = 0 of either players
        for group in s[game_pos_in_state].groups:
            if group.dof == 0:
                return True

        # Tests if there are no more possible actions (draw)
        if(s[game_pos_in_state].actions(s) == []):
            return True

        # Not terminal
        return False

    def utility(self, s, p):
        # Returns 1 if p wins, -1 if p looses, 0 in case of a draw
        # Else returns the score WRT a player

        minDofPlayerOne, minDofPlayerTwo  = 10000, 10000
        i, j = 0, 0
        sumOne = 0
        sumTwo = 0

        # The position of the game variable in the state
        game_pos_in_state = 2 + self.boardSize * self.boardSize

        # Search in game for min DOF and sums DOFs of groups for both players
        for group in s[game_pos_in_state].groups:
            if group.player == 1:
                if(group.dof < minDofPlayerOne):
                    minDofPlayerOne = group.dof

                    # Checking if game has ended at this point
                    if minDofPlayerOne == 0 & p == 0:
                        return -1
                    elif minDofPlayerOne == 0 & p == 1:
                        return 1

                sumOne += group.dof
                i += 1 # counting the number of DOF's summed

            if group.player == 2:
                if group.dof < minDofPlayerTwo:
                    minDofPlayerTwo = group.dof

                    # Checking if game has ended at this point
                    if minDofPlayerTwo == 0 & p == 0:
                        return 1
                    elif minDofPlayerTwo == 0 & p == 1:
                        return -1
                    
                sumTwo += group.dof  
                j += 1 # counting the number of DOF's summed         
     
        # Getting the average DOF of both players
        avgDofPlayerOne = sumOne / i
        avgDofPlayerTwo = sumTwo / j
        
        # Get the maximum possible score for the current board size
        max_score = self.board_max_score(self.boardSize)

        scorePlayerOne = self.calc_solo_score(minDofPlayerOne, avgDofPlayerOne) / max_score
        scorePlayerTwo = self.calc_solo_score(minDofPlayerTwo, avgDofPlayerTwo) / max_score

        # Determining the score WRT a player
        score = scorePlayerOne - scorePlayerTwo
        
        if p == 1:
            return score
        else:
            return -score

    def actions(self, s):
        # Returns a list of valid moves at state s
        possiblePlays = []
        for i in range(0, (self.boardSize * self.boardSize)-2):
            # Check for free spaces in board
            if s[i+2] == 0:
                row = int(i / self.boardSize)
                column = (i % self.boardSize)
                possiblePlays.append([s[1], row, column])
        return possiblePlays

    def result(self, s, a):
        # Returns the sucessor game state after playing move a at state s
        # a is tuple {p, i, j} where p={1,2} is the player, i=0...n is the row and j=0...n is the column

        # Create a copy of the state to prevent changing the original one
        newState = copy.deepcopy(s)

        # The position of the game variable in the state
        game_pos_in_state = 2 + self.boardSize * self.boardSize

        # Convert [row, column] into board index
        piecePos = a[1]*self.boardSize + a[2]

        # Create a group for the new piece
        newGroup = group.Group(newState[game_pos_in_state], newState, piecePos)

        # Add the piece's group ID to the state representation
        newState[piecePos + 2] = newGroup.id

        # Search for possible nearby allied groups to join to
        newState = newGroup.search_nearby_groups(newState, newState[game_pos_in_state], piecePos)

        # Update the next player to move
        if newState[1] == 1:
            newState[1] = 2
        elif newState[1] == 2:
            newState[1] = 1

        return newState

    @classmethod
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
        for piecePos in range(0, self.boardSize * self.boardSize):
            if s[piecePos + 2] != 0:
                # Specify to which player the piece belongs to
                s[1] = s[piecePos + 2]

                # Create a group for the new piece
                newPiece = group.Group(self, s, piecePos)

                # Add the piece's group ID to the state representation
                s[piecePos + 2] = newPiece.id

                # Search for possible nearby allied groups to join to
                s = newPiece.search_nearby_groups(s, self, piecePos, board_init=True)

        return s

    # Gets a position's content from the board
    # Board example:
    # 1 2 3
    # 4 5 6
    # 7 8 9
    def get_board_space(self, s, spaceId):
        return s[spaceId + 2]

    # Set a position's content in the board
    # Board example:
    # 1 2 3
    # 4 5 6
    # 7 8 9
    def set_board_space(self, s, spaceId, value):
        s[spaceId + 2] = value
        return s                

    def find_groups(self, s, newPiece):
        return 1

    def order_moves(self, s, a):
        # Orders list of moves to place best in the beggining and speed up search
        return 1

    # Function that calculates the individual score of each player, without considering the opponent
    @classmethod
    def calc_solo_score(self, minDofPlayer, avgDofPlayer):
        # (weights TBD)
        weightMinPlayer = 0.5
        weightAvgPlayer = 0.5

        # Applying heuristic to one player
        scorePlayer = weightMinPlayer * minDofPlayer + weightAvgPlayer * avgDofPlayer

        return scorePlayer

    # Function that gets the biggest possible score, considering the board size
    @classmethod
    def board_max_score(self, boardSize):
        tmpBoardSize = boardSize
        max_dof = 0
        max_score = 0

        while tmpBoardSize > 1:
            squareSize = tmpBoardSize - 2

            # If the first square was already analysed, we have to build a bridge to connect the squares
            # in the same group. This bridge removes one degree of freedom.
            if max_dof > 0:
                max_dof -= 1

            # Add a bridge if there's still a 2x2 empty block inside the smallest square
            if tmpBoardSize == 2:
                max_dof += 2

            # Check if one can build a square of pieces inside the board, without the outer margin
            if squareSize >= 1:
                # Add the spaces around the square of pieces
                max_dof += 4 * squareSize

                # Get the inner square size
                innerSquareSize = squareSize - 2

                # Check if the inside of the square has empty spaces
                if innerSquareSize > 1:
                    # Add the spaces inside the square of pieces
                    max_dof += innerSquareSize + 2 * (innerSquareSize - 1) + innerSquareSize - 2
                elif innerSquareSize == 1:
                    # Add the space inside the square of pieces
                    max_dof += 1

            # Go to the next square (3 rows bellow, subtract 3 * 2 in the board size)
            tmpBoardSize -= 6

        # Calculate the maximum possible score, considering that the opponent has score 0
        max_score = self.calc_solo_score(max_dof, max_dof)

        return max_score