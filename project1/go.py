'''
state = < n, p, x0, x1, ..., x(n-1), game >

n = board size (example: n=4 corresponds to a 4x4 board)
p = next player to move (p=1 or p=2).

'''

import copy
from operator import itemgetter

class Game:
    """Atari Go game engine"""

    # Declare the variable corresponding to the real state of the game (not the same as in the AI's simulations)
    gameState = []
    
    def __init__(self):
        self.boardSize = 0

        # List of available id's for player groups
        # First row: player one's available group ids
        # Second row: player two's available group ids
        self.freeIds = [[3], [4]]

        # Initialize the groups list as empty
        self.groups = []

        # Declare the variable corresponding to the real state of the game (not the same as in the AI's simulations)
        # self.state = []

    def to_move(self, s):
        # Returns the player to move next given the state s TENHO FOME
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

        # Consider the state in case of being the other player playing
        otherPlayerState = s

        if s[1] == 1:
            otherPlayerState[1] = 2
        else:
            otherPlayerState[1] = 1

        # Tests if there are no more possible actions (draw)
        if s[game_pos_in_state].actions(s) == [] and otherPlayerState[game_pos_in_state].actions(otherPlayerState) == []:
            return 0

        # Search in game for min DOF and sums DOFs of groups for both players
        for group in s[game_pos_in_state].groups:
            if group.player == 1:
                if(group.dof < minDofPlayerOne):
                    minDofPlayerOne = group.dof

                    # Checking if game has ended at this point
                    if minDofPlayerOne == 0 and p == 1:
                        return -1
                    elif minDofPlayerOne == 0 and p == 2:
                        return 1

                sumOne += group.dof
                i += 1 # counting the number of DOF's summed

            if group.player == 2:
                if group.dof < minDofPlayerTwo:
                    minDofPlayerTwo = group.dof

                    # Checking if game has ended at this point
                    if minDofPlayerTwo == 0 and p == 1:
                        return 1
                    elif minDofPlayerTwo == 0 and p == 2:
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
            # Check if the state corresponds to the real one or to a simulation
            if self.get_object_reference(s) == self.get_object_reference(Game.gameState):
                ############# Debug #####################################
                # actionsList = self.sort_actions(s)
                # print("Sorted actions: " str(actionsList))
                # return actionsList
                #########################################################

                # Sort the actions by the utility given in the first move
                return self.sort_actions(s)
            else:
                # Just remove the suicidal moves
                return self.remove_suicides(s)

    # Returns the sucessor game state after playing move a at state s
    # a is tuple (p, i, j) where p={1, 2} is the player, i=1...n is the row and j=1...n is the column
    def result(self, s, a):
        # Create a copy of the state to prevent changing the original one
        newState = copy.deepcopy(s)

        # The position of the game variable in the state
        game_pos_in_state = 2 + self.boardSize * self.boardSize

        # Convert [row, column] into board index
        piecePos = (a[1] - 1)*self.boardSize + a[2] - 1

        player = s[1]

        # Create a group for the new piece
        newGroup = Group(newState[game_pos_in_state], newState, piecePos, player)

        # Add the piece's group ID to the state representation
        newState[piecePos + 2] = newGroup.id

        # Search for possible nearby allied groups to join to
        newState = newGroup.search_nearby_groups(newState, newState[game_pos_in_state], piecePos)

        # Update the next player to move
        if newState[1] == 1:
            newState[1] = 2
        else:
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

        self.boardSize = state[0]

        # Append the Game object to the state representation, allowing copies of the groups inside the AI's simulations
        state.append(self)

        # Group pieces in initial board configuration
        state = self.get_groups(state)

        # Save the real board's state in the game object (to distinguish from the AI's simulated states)
        Game.gameState = state

        return state

    def get_player_score(self, player):
        # Returns player's group of pieces with lowest degrees of freedom
        # 1 -> player 1, 2 -> player 2
        return 1

    def get_groups(self, s):
        for piecePos in range(0, (self.boardSize * self.boardSize) - 1):
            if s[piecePos + 2] != 0:
                # Specify to which player the piece belongs to
                player = s[piecePos + 2]

                # Create a group for the new piece
                newPiece = Group(self, s, piecePos, player)

                # Add the piece's group ID to the state representation
                s[piecePos + 2] = newPiece.id

                # Search for possible nearby allied groups to join to
                s = newPiece.search_nearby_groups(s, self, piecePos, player, board_init=True)

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

    def remove_suicides(self, s, sort=False):
        if sort:
            # Returns a list of suicidal moves at state s
            suicidalPlays = []
        else:
            # Returns a list of valid moves at state s
            possiblePlays = []

        # The position of the game variable in the state
        game_pos_in_state = 2 + self.boardSize * self.boardSize

        # Go through each space of the board
        for i in range(0, self.boardSize * self.boardSize):
            row = int(i / self.boardSize) + 1
            column = i % self.boardSize + 1

            # Flag to check if a move is suicidal
            isSuicidal = False

            # Check for free spaces in board
            if s[i+2] == 0:
                # Check if the neighborhood is all occupied:
                # Check if the space at the right is the wall or is occupied by another piece
                if column == self.boardSize or s[game_pos_in_state].get_board_space(s, i + 1) != 0:
                    # Check if the space at the left is the wall or is occupied by another piece
                    if column == 1 or s[game_pos_in_state].get_board_space(s, i - 1) != 0:
                        # Check if the space bellow is the wall or is occupied by another piece
                        if row == self.boardSize or s[game_pos_in_state].get_board_space(s, i + self.boardSize) != 0:
                            # Check if the space above is the wall or is occupied by another piece
                            if row == 1 or s[game_pos_in_state].get_board_space(s, i - self.boardSize) != 0:
                                # Simulate the current action
                                simState = s[game_pos_in_state].result(s, (s[1], row, column))
                            
                                for group in simState[game_pos_in_state].groups:
                                    # Search for the group of the new piece
                                    if group.id == simState[game_pos_in_state].get_board_space(simState, i):
                                        if group.dof == 0:
                                            isSuicidal = True

                                            # If the actions are being sorted, return the suicidal moves
                                            if sort:
                                                suicidalPlays.append((s[1], row, column))
                                                
                # If the the actions are not being sorted, like in a simulation, return the possible moves
                if not isSuicidal and not sort:
                    possiblePlays.append((s[1], row, column))

        if sort:
            # Returns a list of suicidal moves at state s
            return suicidalPlays
        else:
            # Returns a list of valid moves at state s
            return possiblePlays

    # Sorts list of moves to place best in the beggining and speed up search
    def sort_actions(self, s):
        # List of tuples with the actions to be sorted and their corresponding utility
        # (0.999999 if the opponent could win in his or her next move)
        sortedActions = []

        player = s[1]

        if player == 1:
            opponent = 2
        else:
            opponent = 1

        # Find the moves that would cause the current player to lose
        suicidalPlays = self.remove_suicides(s, sort=True)

        # The position of the game variable in the state
        game_pos_in_state = 2 + self.boardSize * self.boardSize

        # Go through each space of the board
        for i in range(0, self.boardSize * self.boardSize):
            row = int(i / self.boardSize) + 1
            column = i % self.boardSize + 1

            # Check for free spaces in board
            if s[i+2] == 0:
                action = (player, row, column)

                if len(suicidalPlays) > 0:
                    if action == suicidalPlays[0]:
                        # Remove the suicidal action from the list of suicidal actions
                        suicidalPlays = suicidalPlays[1:]

                        # Skip this action
                        continue

                # Simulate the current action
                simState = copy.deepcopy(s)
                simState = simState[game_pos_in_state].result(simState, action)

                # Simulate the current action if it was the opponent playing in that space
                simStateOpponent = copy.deepcopy(s)
                simStateOpponent[1] = opponent
                opponentAction = (opponent, row, column)
                simStateOpponent = simStateOpponent[game_pos_in_state].result(simStateOpponent, opponentAction)

                realPlayerUtility = simState[game_pos_in_state].utility(simState, player)

                # If the opponent could win imediatly, add a big score to occupying that space
                if realPlayerUtility == 1:
                    utilityCurrentPlay = 1
                elif simStateOpponent[game_pos_in_state].utility(simStateOpponent, opponent) == 1:
                    utilityCurrentPlay = 0.999999
                else:
                    utilityCurrentPlay = realPlayerUtility

                # Add the (action, utility) tuple to the list of actions
                actionUtilityTuple = (action, utilityCurrentPlay)
                sortedActions.append(actionUtilityTuple)
            
        # Sort the action tuples in descending order by the utility score
        sortedActions = sorted(sortedActions, key=itemgetter(1), reverse=True)

        # Get only the action from the (action, utility) tuple
        sortedActions = list(map(itemgetter(0), sortedActions))

        return sortedActions

    # Function that calculates the individual score of each player, without considering the opponent
    @classmethod
    def calc_solo_score(self, minDofPlayer, avgDofPlayer):
        # (weights TBD)
        weightMinPlayer = 0.8
        weightAvgPlayer = 0.2

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

    @classmethod
    def get_object_reference(self, obj):
        return hex(id(obj))

    def print_board(self, s, print_ids=False):
        # The position of the game variable in the state
        game_pos_in_state = 2 + self.boardSize * self.boardSize

        print('\n')

        if not print_ids:
            for i in range(2, len(s)-1):
                if s[i] == 0:
                    print(' _ ', end="")
                if s[i] % 2 == 1:
                    print(' X ', end="")
                if s[i] % 2 == 0 and s[i] != 0:
                    print(' O ', end="")
                if ((i-1) % self.boardSize) == 0:
                    print('\n')
        else:
            for i in range(2, len(s)-1):
                if s[i] == 0:
                    print(' _ ', end="")
                else:
                    print(' ' + str(s[game_pos_in_state].get_board_space(s, i-2)) + ' ', end="")
                if ((i-1) % self.boardSize) == 0:
                    print('\n')

        print(s)


##########################################################
#                                                        #
#                                                        #
#       GROUP CLASS                                      #
#                                                        #
#                                                        #
##########################################################

class Group:
    def __init__(self, game, state, piece, player):
        # Degrees of freedom
        self.dof = self.get_piece_dof(game, state, piece)

        # Set the corresponding player
        self.player = player

        # Get the unique ID of the group 
        self.id = game.freeIds[player-1][0]

        # Remove the newly assigned group ID from the list of available group IDs
        if len(game.freeIds[player-1]) > 1: 
            game.freeIds[player-1] = game.freeIds[player-1][1:]
        else:
            # If the new ID is the biggest one available, add the next possible ID
            game.freeIds[player-1][0] = self.id + 2
        
        # Add the new group to the game's list of groups
        game.groups.append(self)

    # Joins two groups and returns the new state and joined group
    def join_group(self, group, game, state, player):
        # Confirm that the two groups to be joined are from the same player
        if self.player != group.player:
            print('ERROR: Can\'t join groups from different players.')
            return None

        # See what's the biggest group, which should be kept
        if(self.get_number_pieces(game, state) > group.get_number_pieces(game, state)):
            big_group = self
            small_group = group
        else:
            big_group = group
            small_group = self

        for i in range(0, game.boardSize * game.boardSize):
            if game.get_board_space(state, i) == small_group.id:
                # Change the small group's pieces IDs to the ID of the big group
                state = game.set_board_space(state, i, big_group.id)

        # Update the new group's degrees of freedom
        big_group.dof = big_group.get_dof(game, state)

        # Temporarly save the ID of the group that will be eliminated
        old_id = small_group.id

        # Delete the old group
        for i in range(0, game.groups.__len__()):
            if game.groups[i].id == old_id:
                del game.groups[i]
                break

        # Add the deleted group's ID to the top of the list of the player's free IDs
        game.freeIds[player-1] = [old_id] + game.freeIds[player-1]

        return [state, big_group]

    # Get the total number of pieces in the group
    def get_number_pieces(self, game, state):
        num_pieces = 0

        for i in range(1, game.boardSize):
            if game.get_board_space(state, i) == self.id:
                num_pieces += 1

        return num_pieces

    # Get the degrees of freedom of one piece
    def get_piece_dof(self, game, state, piece):
        # Maximum possible degrees of freedom for a single piece        
        dof = 4
        piece_row = int(piece / game.boardSize) + 1
        piece_column = piece % game.boardSize + 1

        # Check if the space at the right of the piece exists
        if piece_column < game.boardSize:
            # Check if the space at the right of the piece is occupied
            if game.get_board_space(state, piece + 1) != 0:
                dof -= 1
        else:
            dof -= 1

        # Check if the space at the left of the piece exists
        if piece_column > 1:
            # Check if the space at the left of the piece is occupied
            if game.get_board_space(state, piece - 1) != 0:
                dof -= 1
        else:
            dof -= 1

        # Check if the space above the piece exists
        if piece_row > 1:
            # Check if the space above the piece is occupied
            if game.get_board_space(state, piece - game.boardSize) != 0:
                dof -= 1
        else:
            dof -= 1

        # Check if the space bellow the piece exists
        if piece_row < game.boardSize:
            # Check if the space bellow the piece is occupied
            if game.get_board_space(state, piece + game.boardSize) != 0:
                dof -= 1
        else:
            dof -= 1

        return dof

    # Get the degrees of freedom of one group
    def get_dof(self, game, state):
        dof = 0

        # Set of empty spaces adjacent to the group; Using a set to avoid duplicates
        adjacentEmptySpaces = set([])

        for i in range(0, game.boardSize * game.boardSize):
            if game.get_board_space(state, i) == self.id:
                piece_row = int(i / game.boardSize) + 1
                piece_column = i % game.boardSize + 1

                # Check if the space at the right of the piece exists
                if piece_column < game.boardSize:
                    # Check if the space at the right of the piece is empty
                    if game.get_board_space(state, i + 1) == 0:
                        # Add to the set of empty spaces near the group
                        adjacentEmptySpaces.add(i + 1)

                # Check if the space at the left of the piece exists
                if piece_column > 1: 
                    # Check if the space at the left of the piece is empty
                    if game.get_board_space(state, i - 1) == 0:
                        # Add to the set of empty spaces near the group
                        adjacentEmptySpaces.add(i - 1)

                # Check if the space above the piece exists
                if piece_row > 1:
                    # Check if the space above the piece is empty
                    if game.get_board_space(state, i - game.boardSize) == 0:
                        # Add to the set of empty spaces near the group
                        adjacentEmptySpaces.add(i - game.boardSize)

                # Check if the space bellow the piece exists
                if piece_row < game.boardSize:
                    # Check if the space bellow the piece is empty
                    if game.get_board_space(state, i + game.boardSize) == 0:
                        # Add to the set of empty spaces near the group
                        adjacentEmptySpaces.add(i + game.boardSize)

        # The degrees of freedom is the number of empty spaces adjacent to the group
        dof = len(adjacentEmptySpaces)

        return dof

    # Search groups that are nearby the piece index, to see if joins or degree of freedom 
    # subtractions are needed.
    # - state: Current state of the game, according to the designated representation.
    # - game: Object that contains the most important game data and methods.
    # - piece: Board index of the piece being analysed.
    # - board_init: Boolean that tells wether the function is being called when initializing
    # a board (True) or if it's when a new piece is being added to an already seen board (False).
    def search_nearby_groups(self, state, game, piece, player=-1, board_init=False):
        piece_row = int(piece / game.boardSize) + 1
        piece_column = piece % game.boardSize + 1

        # List of groups that the new pieced affected (by decreasing the degrees of freedom)
        groupsDofChanged = []

        # List of groups that the new piece joined to
        groupsJoined = []

        if not board_init:
            player = state[1]

        # Real group, that can be changed upon group join
        real_group = self

        # Check if the space at the right of the piece exists
        if piece_column < game.boardSize:
            # Check if the space at the right of the piece is occupied with an allied piece
            if game.get_board_space(state, piece + 1) != 0:
                if game.get_board_space(state, piece + 1) % 2 == (self.player % 2):
                    # Join group of the same player
                    for group in game.groups:
                        if group.id == game.get_board_space(state, piece + 1):
                            # Join the groups
                            [state, real_group] = real_group.join_group(group, game, state, player)

                            # Add the joined group ID to the list of joined groups (avoid redundant and dangerous rejoins)
                            groupsJoined.append(group.id)
                            break
                # Check if right side has different "parity" and it's not loading the board 
                elif game.get_board_space(state, piece + 1) % 2 != (self.player % 2) and not board_init:
                    # Subtract a degree of freedom from the adjacent opponent group
                    for group in game.groups:
                        if group.id == game.get_board_space(state, piece + 1):
                            # Decrease the adjacent group's degrees of freedom
                            group.dof -= 1

                            # Add the affected groups ID to the list of affected groups (avoid decreasing DOF again)
                            groupsDofChanged.append(group.id)

        # Check if the space at the left of the piece exists
        if piece_column > 1:
            # Check if the space at the left of the piece is occupied with an allied piece
            if game.get_board_space(state, piece - 1) != 0:
                # Check if the piece at the left is of the same player
                # and was not previously joined in the same group
                if game.get_board_space(state, piece - 1) % 2 == (self.player % 2) \
                   and not game.get_board_space(state, piece - 1) in groupsJoined: 
                    # Join group of the same player
                    for group in game.groups:
                        if group.id == game.get_board_space(state, piece - 1):                  
                            # Join the groups
                            [state, real_group] = real_group.join_group(group, game, state, player)

                            # Add the joined group ID to the list of joined groups (avoid redundant and dangerous rejoins)
                            groupsJoined.append(group.id)
                            break
                # Check if left side has different "parity", 
                # it's not loading the board 
                # and the group wasn't previously affected
                elif game.get_board_space(state, piece - 1) % 2 != (self.player % 2) \
                     and not board_init \
                     and not game.get_board_space(state, piece - 1) in groupsDofChanged:
                    # Subtract a degree of freedom from the adjacent opponent group
                    for group in game.groups:
                        if group.id == game.get_board_space(state, piece - 1):
                            # Decrease the adjacent group's degrees of freedom
                            group.dof -= 1

                            # Add the affected groups ID to the list of affected groups (avoid decreasing DOF again)
                            groupsDofChanged.append(group.id)

        # Check if the space above the piece exists
        if piece_row > 1:
            # Check if the space above the piece is occupied with an allied piece
            if game.get_board_space(state, piece - game.boardSize) != 0:
                # Check if the piece above is of the same player
                # and was not previously joined in the same group
                if game.get_board_space(state, piece - game.boardSize) % 2 == (self.player % 2) \
                   and not game.get_board_space(state, piece - game.boardSize) in groupsJoined: 
                    # Join group of the same player
                    for group in game.groups:
                        if group.id == game.get_board_space(state, piece - game.boardSize):
                            # Join the groups
                            [state, real_group] = real_group.join_group(group, game, state, player)

                            # Add the joined group ID to the list of joined groups (avoid redundant and dangerous rejoins)
                            groupsJoined.append(group.id)
                            break
                # Check if the piece above has different "parity", 
                # it's not loading the board 
                # and the group wasn't previously affected
                elif game.get_board_space(state, piece - game.boardSize) % 2 != (self.player % 2) \
                     and not board_init \
                     and not game.get_board_space(state, piece - game.boardSize) in groupsDofChanged:
                    # Subtract a degree of freedom from the adjacent opponent group
                    for group in game.groups:
                        if group.id == game.get_board_space(state, piece - game.boardSize):
                            # Decrease the adjacent group's degrees of freedom
                            group.dof -= 1

                            # Add the affected groups ID to the list of affected groups (avoid decreasing DOF again)
                            groupsDofChanged.append(group.id)

        # Check if the space bellow the piece exists
        if piece_row < game.boardSize:
            # Check if the space bellow the piece is occupied with an allied piece
            if game.get_board_space(state, piece + game.boardSize) != 0:
                # Check if the piece bellow is of the same player
                # and was not previously joined in the same group
                if game.get_board_space(state, piece + game.boardSize) % 2 == (self.player % 2) \
                   and not game.get_board_space(state, piece + game.boardSize) in groupsJoined: 
                    # Join group of the same player
                    for group in game.groups:
                        if group.id == game.get_board_space(state, piece + game.boardSize):
                            # Join the groups
                            [state, real_group] = real_group.join_group(group, game, state, player)

                            # Add the joined group ID to the list of joined groups (avoid redundant and dangerous rejoins)
                            groupsJoined.append(group.id)
                            break
                # Check if the piece bellow has different "parity", 
                # it's not loading the board 
                # and the group wasn't previously affected
                elif game.get_board_space(state, piece + game.boardSize) % 2 != (self.player % 2) \
                     and not board_init \
                     and not game.get_board_space(state, piece + game.boardSize) in groupsDofChanged:
                    # Subtract a degree of freedom from the adjacent opponent group
                    for group in game.groups:
                        if group.id == game.get_board_space(state, piece + game.boardSize):
                            # Decrease the adjacent group's degrees of freedom
                            group.dof -= 1

                            # Add the affected groups ID to the list of affected groups (avoid decreasing DOF again)
                            groupsDofChanged.append(group.id)

        return state