import random

BOARD_SIZE = 10
MINE_CHAR = '*'
INITIAL_CHAR = 'x'
ALL_DIRECTIONS = [ (-1,-1), (-1,0), (-1,1),
                (0,-1), (0,1),
                (1,-1), (1,0), (1,1) ]
HORIZONTAL_VERTICAL_DIRECTIONS = [  (-1,0), 
                (0,-1), (0,1),
                 (1,0),  ]
MAX_MINES = 35

class board_state:

    def __init__(self):
        self.cells = [INITIAL_CHAR]*(BOARD_SIZE**2)
        self.cleared_cells = 0        
        self.cleared_cells_needed_to_win = 0
        self.generate_random_mines()

    # get board state as a string
    def __str__(self):
        ret = '-'*(BOARD_SIZE*2+1) + '\n'
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                # hide the mines
                cell = y*BOARD_SIZE + x                
                ret += '|'
                if( not self.is_cell_a_mine(y,x) ):
                    ret += self.cells[cell] 
                else:
                    ret += INITIAL_CHAR
            
            ret += '|'
            ret += '\n'
            ret += '-'*(BOARD_SIZE*2+1) + '\n'
        return ret

    # flood-fill a selection
    def flood_fill_cell_selection(self, row, col):

        # base case, ensure that we do not attempt
        # to flood-fill out of bounds nor mines
        cell_coordinate = row*BOARD_SIZE + col
        if (self.is_cell_coordinate_inbounds( row, col ) 
            and not self.is_cell_a_mine( row, col ) 
            and self.cells[ cell_coordinate ] == 'x'):
            x = self.get_number_of_nearby_mines(row, col)
            self.cells[cell_coordinate] = chr( x + ord('0')) if x != 0 else ' '
            self.cleared_cells += 1
        else:
            return

        # recurse in horizontal and vertical directions
        for x, y in HORIZONTAL_VERTICAL_DIRECTIONS:
            temp_row, temp_col = row + y, col + x
            self.flood_fill_cell_selection(temp_row, temp_col)
            

    # get nearby mines given cell coordinates
    def get_number_of_nearby_mines(self, row, col):
        ret = 0
        for x,y in ALL_DIRECTIONS:
            temp_row, temp_col = row + y, col + x
            ret += int(self.is_cell_a_mine(temp_row, temp_col))
        return ret

    # build initial state
    def generate_random_mines(self):
        random.seed()
        mines = 0
        for x in range(MAX_MINES):
            
            cell_coordinate = random.randint(0, BOARD_SIZE**2 - 1)

            # count the number of mines placed
            if( self.cells[cell_coordinate] != '*' ):
                mines += 1

            self.cells[ cell_coordinate ] = MINE_CHAR

        # set the number of cleared cells to satisfy the win condition
        self.cleared_cells_needed_to_win = BOARD_SIZE**2 - mines

    # check bounds
    def is_cell_coordinate_inbounds(self, row, col):
        return (row >= 0 and row < BOARD_SIZE
                and col >= 0 and col < BOARD_SIZE)

    # check cell is a mine
    def is_cell_a_mine(self, row, col):
        return (self.is_cell_coordinate_inbounds(row, col) and 
                self.cells[row*BOARD_SIZE + col] == MINE_CHAR)

    # check that the win condition has been satisfied
    def won_game(self):
        return self.cleared_cells == self.cleared_cells_needed_to_win

class game:

    def __init__(self):
        self.game_is_on = True
        self.game_board = board_state()

    # check cell is a mine
    def is_cell_a_mine(self, row, col):
        return self.game_board.is_cell_a_mine(row, col)


    # get player input
    def retrieve_player_input(self):

        # assume player input isn't messy
        # TODO improve
        message = "Enter your move in x y coordinates:"
        row, col = -1,-1
        while( not self.game_board.is_cell_coordinate_inbounds(row, col) ):
            try:
                row,col = map(int,input(message).split())

                if( not self.game_board.is_cell_coordinate_inbounds(row, col) ):
                    print("Invalid input, please try again!")

            except Exception as err:
                print("Invalid input, please try again!")
                continue
        return (row,col)

    # player turn
    def player_turn(self):

        # print the board
        print(self.game_board)
        
        # get player input
        row, col = self.retrieve_player_input()

        # check whether the selection is a mine
        if(self.is_cell_a_mine(row, col)):
            self.lose_game()
            return

        # the game isn't over, flood-fill
        # the player selection, display the board state
        # to the user, and continue
        self.game_board.flood_fill_cell_selection(row, col)

        # check whether we've won or not
        if( self.game_board.won_game() ):
            self.win_game()


    # lose game
    def lose_game(self):
        print("You lose!")
        self.game_is_on = False

    # win game
    def win_game(self):
        # print the board
        print(self.game_board)
        print("You win!")
        self.game_is_on = False

    # start game
    def start_game(self):
        print("Welcome to minesweeper!")


game = game()
game.player_turn()
while game.game_is_on:
    game.player_turn()