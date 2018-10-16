class Group:
    def __init__(self, game, state, piece):
        # Degrees of freedom
        self.dof = self.get_dof(game, state, piece)

        # Set the corresponding player
        self.player = game.nextPlayer

        # Get the unique ID of the group
        self.id = game.freeIds[game.nextPlayer]

        # Remove the newly assigned group ID from the list of available group IDs
        if len(game.freeIds[game.nextPlayer]) > 1:
            game.freeIds[game.nextPlayer] = game.freeIds[game.nextPlayer][1:]
        else:
            # If the new ID is the biggest one available, add the next possible ID
            game.freeIds[game.nextPlayer] = self.id + 2

        # Add the new group to the game's list of groups
        game.groups.append(self)

    def join_group(self, group, game, state):
        # Confirm that the two groups to be joined are from the same player
        if self.player != group.player:
            print('ERROR: Can\'t join groups from different players.')
            return None

        # See what's the biggest group, which should be kept
        if(self.get_number_pieces(game) > group.get_number_pieces(game)):
            big_group = self
            small_group = group
        else:
            big_group = group
            small_group = self

        # New group's degrees of freedom
        dof = 0

        for i in range(1, game.boardSize):
            if game.get_board_space(state, i) == big_group.id:
                # Add the piece's degrees of freedom to the group's value
                dof += self.get_dof(game, state, i)

            if game.get_board_space(state, i) == small_group.id:
                # Change the small group's pieces IDs to the ID of the big group
                state = game.set_board_space(state, i, big_group.id)

                # Add the piece's degrees of freedom to the group's value
                dof += self.get_dof(game, state, i)

        # Update the new group's degrees of freedom
        big_group.dof = dof

        # Delete the old group
        for g in game.groups:
            if g.id == small_group.id:
                del g

        # Add the deleted group's ID to the top of the list of the player's free IDs
        game.freeIds[game.nextPlayer] = small_group.id + game.freeIds[game.nextPlayer]

        # Delete the old group
        del small_group

        return state

    # Get the total number of pieces in the group
    def get_number_pieces(self, game):
        num_pieces = 0

        for i in range(1, game.boardSize):
            if game.set_board_space(i) == self.id:
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

    def search_nearby_groups(self, state, game, piece):
        piece_row = piece / game.boardSize
        piece_column = piece % game.boardSize

        # Check if the space at the right of the piece exists
        if piece_column < game.boardSize:
            # Check if the space at the right of the piece is occupied with an allied piece
            if game.get_board_space(piece + game.boardSize, state) != 0 and \
               game.get_board_space(piece + 1, state) % 2 == self.player % 2:
                for group in game.groups:
                    if group.id == game.get_board_space(piece + 1, state):
                        # Join the groups
                        self.join_group(group, game, state)

        # Check if the space at the left of the piece exists
        if piece_column > 0:
            # Check if the space at the left of the piece is occupied with an allied piece
            if game.get_board_space(piece + game.boardSize, state) != 0 and \
               game.get_board_space(piece - 1, state) % 2 == self.player % 2:
                for group in game.groups:
                    if group.id == game.get_board_space(piece - 1, state):
                        # Join the groups
                        self.join_group(group, game, state)

        # Check if the space above the piece exists
        if piece_row > 0:
            # Check if the space above the piece is occupied with an allied piece
            if game.get_board_space(piece + game.boardSize, state) != 0 and \
               game.get_board_space(piece - game.boardSize, state) % 2 == self.player % 2:
                for group in game.groups:
                    if group.id == game.get_board_space(piece - game.boardSize, state):
                        # Join the groups
                        self.join_group(group, game, state)

        # Check if the space bellow the piece exists
        if piece_row < game.boardSize:
            # Check if the space bellow the piece is occupied with an allied piece
            if game.get_board_space(piece + game.boardSize, state) != 0 and \
               game.get_board_space(piece + game.boardSize, state) % 2 == self.player % 2:
                for group in game.groups:
                    if group.id == game.get_board_space(piece + game.boardSize, state):
                        # Join the groups
                        self.join_group(group, game, state)

        return state