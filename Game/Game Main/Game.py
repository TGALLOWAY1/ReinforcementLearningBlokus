
# Here we put it all together and implement the Game class. It handles the Board, the Players, and the Shapes created above. Note that Players are only able to propose moves, but the Game implements them and updates the Board.

# <codecell>

# Here we implement a very general Game class.
# A Game needs a list of Players, which have functionalities
# that can play according to their strategies.
#
# A Game also takes in an interface called a "board" here
# for convenience, although it should be noted that it can be something
# like a deck of cards as well. The Players can only change the
# board according to the rules of the game.
#
# The Game also has a function that checks if the game has been
# won yet. This must be defined through inheriting the Game class
# and overriding dummy methods for a particular game (e.g. Blokus).
# By inheriting from a Game class, one must define rules that
# check if a move proposed by the Players on the Interface is
# valid or not for a specific game.
#
# The Game also keeps track of the number of rounds that have been
# played. Finally, the Game gives players the chance to play
# cyclically, starting with the first player in the list of players
# when the Game is instantiated.
# GLOBAL VARIABLES:

All_Shapes = [I1(), I2(), I3(), I4(), I5(), \
              V3(), L4(), Z4(), O4(), L5(), \
              T5(), V5(), N(), Z5(), T4(), \
              P(), W(), U(), F(), X(), Y()]

All_Degrees = [0, 90, 180, 270]

All_Flip = ['h', "None"]


class Game:
    """
    A class that takes a list of players objects,
    and a board object and plays moves, keeping track of the number
    of rounds that have been played and determining the validity
    of moves proposed to the game.
    """

    def __init__(self, players, board, all_pieces):
        self.players = players
        self.rounds = 0
        self.board = board
        self.all_pieces = all_pieces

    def winner(self):
        """
        Checks the conditions of the game
        to see if the game has been won yet
        and returns "None" if the game has
        not been won, and the name of the
        player if it has been won.
        """
        return ("None")

    def valid_move(self, player, move):
        """
        Uses functions from the board to see whether
        a player's proposed move is valid.
        """
        return (True)

    def play(self):
        """
        Plays a list of Player objects sequentially,
        as long as the game has not been won yet,
        starting with the first player in the list at
        instantiation.
        """
        if self.rounds == 0:
            # When the game has not begun yet, the game must
            # give the players their pieces and a corner to start.
            max_x = ((self.board).size[1] - 1)
            max_y = ((self.board).size[0] - 1)
            starts = [(0, 0), (max_y, max_x), (0, max_x), (max_y, 0)]

            for i in xrange(len(self.players)):
                (self.players[i]).add_pieces(self.all_pieces)
                (self.players[i]).start_corner(starts[i])

        # if there is no winner, print out the current player's name and
        # let current player perform a move
        if self.winner() == "None":
            current = self.players[0]
            print
            "Current player: " + current.name
            proposal = current.do_move(self)
            if proposal == None:
                # move on to next player, increment rounds
                first = (self.players).pop(0)
                self.players = self.players + [first]
                self.rounds += 1


            # ensure that the proposed move is valid
            elif self.valid_move(current, proposal.points):
                # update the board with the move
                (self.board).update(current, proposal.points)
                # let the player update itself accordingly
                current.update_player(proposal, self.board)
                # remove the piece that was played from the player
                current.remove_piece(proposal)
                # place the player at the back of the queue
                first = (self.players).pop(0)
                self.players = self.players + [first]
                # increment the number of rounds just played
                self.rounds += 1

            # interrupts the game if an invalid move is proposed
            else:
                raise Exception("Invalid move by " + current.name + ".")

        else:
            print
            "Game over! And the winner is: " + self.winner()


# <codecell>

# Here we inherit the Game class in order to
# create the Blokus game. Functions like "play" remain
# the same, but "valid_move" and "winner" are overwritten
# according to the rules of Blokus.

class Blokus(Game):
    """
    A class that takes a list of players, e.g. ['A','B','C'],
    and a board and plays moves, keeping track of the number
    of rounds that have been played.
    """

    def winner(self):
        """
        Checks the conditions of the game
        to see if the game has been won yet
        and returns "None" if the game has
        not been won, and the name of the
        player if it has been won.
        """
        # Credit to Dariusz Walczak for inspiration.
        # http://stackoverflow.com/questions/1720421/merge-two-lists-in-python
        moves = [p.possible_moves(p.pieces, self) for p in self.players]
        if False in [mv == [] for mv in moves]:
            return ("None")
        else:
            cand = [(p.score, p.name) for p in self.players]
            return (sorted(cand, reverse=True)[0][1])

    def valid_move(self, player, move):
        """
        Uses functions from the board to see whether
        a player's proposed move is valid.
        """
        if self.rounds < len(self.players):
            if ((False in [(self.board).in_bounds(pt) for pt in move])
                    or (self.board).overlap(move)
                    or not (True in [(pt in player.corners) for pt in move])):
                return (False)
            else:
                return (True)

        elif ((False in [(self.board).in_bounds(pt) for pt in move])
              or (self.board).overlap(move)
              or (self.board).adj(player, move)
              or not (self.board).corner(player, move)):
            return (False)

        else:
            return (True)
