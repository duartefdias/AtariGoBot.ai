class Group:

    def __init__(self, piece, player):
        self.pieces = [piece]
        self.dof = 0 #Degrees of freedom
        self.player = player

    def join_group(self, group):
        self.pieces.append(group.pieces)
        self.pieces += group.dof - 1

    def add_piece(self, piece):
        self.pieces.append(piece)