
# BOARD

# <codecell>

# Playing Blokus requires an interface.
# Our interface is a square board, which we will
# represent as a list of lists.
#
#      e.g. [[1,2],[3,4]] is the following board:
#
#           | 1 2 |
#           | 3 4 |
#
# Write a function that lets us print such a board.

def printBoard(board):
    n = 2
    """
    Prints the board where the representation of a board is
    a list of row-lists. The function throws an error if the
    the board is invalid: the length of the rows are not
    the same.
    """
    assert (len(set([len(board[i]) for i in xrange(len(board))])) == 1)
    print
    ' ' * n,
    for i in range(len(board[1])):
        print
        str(i) + ' ' * (n - len(str(i))),
    print
    for i, row in enumerate(board):
        print
        str(i) + ' ' * (n - len(str(i))), (' ' * n).join(row)




# <codecell>

# This function uses MatplotLib to create a fancy image
# of the board that opens in a separate window.

def fancyBoard(board, num):
    Apoints = []
    Bpoints = []

    for y in enumerate(board.state):
        for x in enumerate(y[1]):
            if x[1] == "A":
                Apoints.append((x[0], (board.size[0] - 1) - y[0]))
            if x[1] == "B":
                Bpoints.append((x[0], (board.size[0] - 1) - y[0]))

    # fig = plt.figure(frameon=False)
    ax = plt.subplot(111, xlim=(0, board.size[0]), ylim=(0, board.size[1]))

    for i in xrange(board.size[0] + 1):
        for j in xrange(board.size[1] + 1):
            polygon = plt.Polygon([[i, j], [i + 1, j], [i + 1, j + 1], [i, j + 1], [i, j]])
            if (i, j) in Apoints:
                polygon.set_facecolor('red')
                ax.add_patch(polygon)
            elif (i, j) in Bpoints:
                polygon.set_facecolor('blue')
                ax.add_patch(polygon)
            else:
                polygon.set_facecolor('lightgrey')
                ax.add_patch(polygon)

    for axis in (ax.xaxis, ax.yaxis):
        axis.set_major_formatter(plt.NullFormatter())
        axis.set_major_locator(plt.NullLocator())

    plt.savefig("random" + str(num) + ".png")
    # plt.show()
    # return ax

# TODO: http://jakevdp.github.io/blog/2012/12/06/minesweeper-in-matplotlib/


class Board:
    """
    Creates a board that has n rows and
    m columns with an empty space represented
    by a character string according to null of
    character length one.
    """

    def __init__(self, n, m, null):
        self.size = (n, m)
        self.null = null
        self.empty = [[self.null] * m for _ in range(n)]
        self.state = self.empty

    def update(self, player, move):
        """
        Takes in a Player object and a move as a
        list of integer tuples that represent the piece.
        """
        for row in range(len(self.state)):
            for col in range(len(self.state[1])):
                if (col, row) in move:
                    self.state[row][col] = player.label

    def in_bounds(self, point):
        """
        Takes in a tuple and checks if it is in the bounds of
        the board.
        """
        return (0 <= point[0] <= (self.size[1] - 1)) & (0 <= point[1] <= (self.size[0] - 1))

    def overlap(self, move):
        """
        Returns a boolean for whether a move is overlapping
        any pieces that have already been placed on the board.
        """
        if False in [(self.state[j][i] == self.null) for (i, j) in move]:
            return True
        else:
            return False

    def corner(self, player, move):
        """
        Note: ONLY once a move has been checked for adjacency, this
        function returns a boolean; whether the move is cornering
        any pieces of the player proposing the move.
        """
        validates = []

        for (i, j) in move:
            if self.in_bounds((j + 1, i + 1)):
                validates.append((self.state[j + 1][i + 1] == player.label))

            if self.in_bounds((j - 1, i - 1)):
                validates.append((self.state[j - 1][i - 1] == player.label))

            if self.in_bounds((j - 1, i + 1)):
                validates.append((self.state[j - 1][i + 1] == player.label))

            if self.in_bounds((j + 1, i - 1)):
                validates.append((self.state[j + 1][i - 1] == player.label))

        if True in validates:
            return True
        else:
            return False

    def adj(self, player, move):
        """
        Checks if a move is adjacent to any squares on
        the board which are occupied by the player
        proposing the move and returns a boolean.
        """
        validates = []

        for (i, j) in move:
            if self.in_bounds((j, i + 1)):
                validates.append((self.state[j][i + 1] == player.label))

            if self.in_bounds((j, i - 1)):
                validates.append((self.state[j][i - 1] == player.label))

            if self.in_bounds((j - 1, i)):
                validates.append((self.state[j - 1][i] == player.label))

            if self.in_bounds((j + 1, i)):
                validates.append((self.state[j + 1][i] == player.label))

        if True in validates:
            return True
        else:
            return False

    def print_board(self, num=None, fancy=False):
        if not fancy:
            printBoard(self.state)
        else:
            fancyBoard(self, num)