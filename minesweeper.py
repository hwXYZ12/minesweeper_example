import sys
import time
import os
import curses
import random
from curses import wrapper

BOARD_SIZE=25
MAX_MINES=300
INITIAL_CHAR = 'x'
UNCOVERED_CHAR = ' '
MINE_CHAR = '*'
UP,RIGHT,DOWN,LEFT,ENTER = 259,261,258,260,10
CURSOR_DIRECTIONS = { UP : (0,-1), RIGHT : (1,0), DOWN : (0,1), LEFT : (-1,0) }
ALL_DIRECTIONS = [ (1,-1), (1,0), (1,1),
					(0,-1), (0,1),
					(-1,-1), (-1,0), (-1,1) ]
HORIZONTAL_VERTICAL_DIRECTIONS = [ (1,0), (-1,0), (0,1), (0,-1) ]
X_MAX = BOARD_SIZE*2
Y_MAX = BOARD_SIZE*2

class board_state:
	
	def __init__(self):
		self.cells = [INITIAL_CHAR]*(BOARD_SIZE**2)
		self.cells_uncovered = 0
		self.cells_required_to_uncover_to_win = 0
		self.fill_with_mines()

	def get_board_state_as_list(self):
		ret=[]
		new_line ='-'*(2*BOARD_SIZE+1)
		ret.append(new_line)
		for y in range(BOARD_SIZE):
			new_line = "|"
			for x in range(BOARD_SIZE):
				cell = y*BOARD_SIZE+x
				# keep mines covered
				char_to_write = (
					self.cells[cell]
					if self.cells[cell] != MINE_CHAR
					else
					INITIAL_CHAR
				)				
				new_line+=char_to_write+'|'
			ret.append(new_line)
			new_line ='-'*(2*BOARD_SIZE+1)
			ret.append(new_line)
		return ret

	# recursively uncover selections
	def flood_fill_selection(self, row, col):

		# base case
		cell = row*BOARD_SIZE+col
		if (not self.is_a_mine(row, col)
			and self.is_inbounds(row, col)
			and self.cells[cell] == INITIAL_CHAR):
			num_mines = self.determine_nearby_mines(row,col)
			self.cells[cell] = chr(ord('0') + num_mines) if num_mines != 0 else UNCOVERED_CHAR
			self.cells_uncovered += 1
		else:
			return

		# recurse in horizontal and vertical directions		
		for a,b in HORIZONTAL_VERTICAL_DIRECTIONS:
			temp_row, temp_col = row + a, col + b
			self.flood_fill_selection(temp_row, temp_col)
 
	def is_inbounds(self, row, col):
		return (row >= 0 and row < BOARD_SIZE
				and col >= 0 and col < BOARD_SIZE)

	def is_a_mine(self, row, col):
		return (self.is_inbounds(row,col) and 
				self.cells[row*BOARD_SIZE+col] == MINE_CHAR)

	def determine_nearby_mines(self, row, col):
		ret = 0
		for a,b in ALL_DIRECTIONS:
			temp_row, temp_col = row + a, col + b
			ret += self.is_a_mine(temp_row, temp_col)
		return ret

	def fill_with_mines(self):
		random.seed()
		mines = 0
		for x in range(MAX_MINES):
			cell = random.randint(0, BOARD_SIZE**2 - 1)
			if( self.cells[cell] != MINE_CHAR):
				mines+=1
			self.cells[cell] = MINE_CHAR
		self.cells_required_to_uncover_to_win = (
			len(self.cells) - mines
		)

	def is_game_won(self):
		return self.cells_uncovered == self.cells_required_to_uncover_to_win
	

class game:

	def __init__(self, stdscr):
		self.stdscr = stdscr
		self.game_is_running = True
		self.board = board_state()

	# checks that the selection is a cell to check
	def is_cell_coord(self, y,x):
		return ((y >= 1 and y <= Y_MAX - 1)
			and (x >= 1 and x <= X_MAX - 1
				and x % 2 == 1))

	# don't use without checking that the coordinates
	# are also cell coordinates
	def convert_to_cell_coord(self, y,x):
		col = (x - 1)//2
		row = (y - 1)//2
		return (row, col)

	def convert_to_cursor_coords(self, row, col):
		x = 2*col + 1
		y = 2*row + 1
		return (y, x)

	def check_mine(self, y, x):
		row, col = self.convert_to_cell_coord(y,x)

		# check that this selection is not a mine
		if( self.board.is_a_mine(row, col) ):
			self.lose_game()
		else:
			# flood fill the selection
			self.board.flood_fill_selection(row, col)

		# check for the win condition
		if( self.board.is_game_won() ):
			self.win_game()
		
	
	# handle player input
	def player_turn(self):
		pressed = self.stdscr.getch()
		y,x = self.stdscr.getyx()
		if pressed == ENTER:
			if( self.is_cell_coord(y,x)):
				self.check_mine(y,x)
		elif pressed in CURSOR_DIRECTIONS:
			# move the cursor to a new position
			inc_x, inc_y = CURSOR_DIRECTIONS[pressed]
			x += inc_x
			y += inc_y
			
			# bound cursor
			if x > X_MAX: x = X_MAX
			if y > Y_MAX: y = Y_MAX
			if x < 0: x = 0
			if y < 0: y = 0

			# move cursor to the new position
			self.stdscr.move(y,x)

	def is_game_on(self):
		return self.game_is_running

	def lose_game(self):
		
		# clear the screen
		self.stdscr.clear()

		self.game_is_running = False

		# print to user
		self.stdscr.addstr("You lost!")
		self.stdscr.refresh()

	def win_game(self):
		
		# clear the screen
		self.stdscr.clear()

		self.game_is_running = False

		# print to user
		self.stdscr.addstr("You won!")
		self.stdscr.refresh()

	def get_board_to_write(self):
		return self.board.get_board_state_as_list()



def write_board(stdscr, board):

	# save cursor position
	y,x = stdscr.getyx()

	# clear screen
	stdscr.clear()

	for i in range(len(board)):
		stdscr.addstr(i,0,board[i])

	# refresh screen
	stdscr.refresh()

	# move the cursor back to it's original position
	stdscr.move(y,x)

def main(stdscr):

	# clear screen
	stdscr.clear()

	# main game loop
	main_game = game(stdscr)
	while(main_game.is_game_on()):
		write_board(stdscr, main_game.get_board_to_write())
		main_game.player_turn()

	# await user input
	stdscr.getch()	

wrapper(main)
