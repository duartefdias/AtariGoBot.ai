class Group:
    def __init__(self, game, state, piece):
        # Get the unique ID of the group
        self.id = game.freeIds[game.nextPlayer]

        # Degrees of freedom
        self.dof = self.get_dof(game, state, piece)

        # Add the ide
        self.player = game.nextPlayer

        # Remove the newly assigned group ID from the list of available group IDs
        if len(game.freeIds[game.nextPlayer]) > 1:
            game.freeIds[game.nextPlayer] = game.freeIds[game.nextPlayer][1:]
        else:
            # If the new ID is the biggest one available, add the next possible ID
            game.freeIds[game.nextPlayer] = self.id + 2

        # Add the new group to the game's list of groups
        game.groups.append(self)

    def join_group(self, group, game, state):
        # See what's the biggest group, which should be kept
        if(self.get_number_pieces(game) > group.get_number_pieces(game)):
            big_group = self
            small_group = group
        else:
            big_group = group
            small_group = self

        

    # Get the total number of pieces in the group
    def get_number_pieces(self, game):
        num_pieces = 0

        for i in range(1, game.boardSize):
            if game.get_board_space(i) == self.id:
                num_pieces += 1

        return num_pieces

    def get_dof(self, game, state, piece):
        # Maximum possible degrees of freedom for a single piece
        dof = 4

        piece_row = piece / game.boardSize
        piece_column = piece % game.boardSize

        # Check if the space at the right of the piece exists
        if piece_column < game.boardSize:
            # Check if the space at the right of the piece is occupied
            if game.get_board_space(piece + 1, state) != 0:
                dof -= 1
        else:
            dof -= 1

        # Check if the space at the left of the piece exists
        if piece_column > 0:
            # Check if the space at the left of the piece is occupied
            if game.get_board_space(piece - 1, state) != 0:
                dof -= 1
        else:
            dof -= 1

        # Check if the space above the piece exists
        if piece_row > 0:
            # Check if the space above the piece is occupied
            if game.get_board_space(piece - game.boardSize, state) != 0:
                dof -= 1
        else:
            dof -= 1

        # Check if the space bellow the piece exists
        if piece_row < game.boardSize:
            # Check if the space bellow the piece is occupied
            if game.get_board_space(piece + game.boardSize, state) != 0:
                dof -= 1
        else:
            dof -= 1

        return dof