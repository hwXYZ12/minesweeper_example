import sys
import time
import os
import curses
from curses import wrapper

BOARD_SIZE=10
UP,RIGHT,DOWN,LEFT,ENTER = 259,261,258,260,10
DIRECTIONS = { UP : (0,-1), RIGHT : (1,0), DOWN : (0,1), LEFT : (-1,0) }
X_MAX = BOARD_SIZE*2
Y_MAX = BOARD_SIZE+1

class game:

	def __init__(self, stdscr):
		self.stdscr = stdscr
	
	# handle player input
	def player_turn(self):
		pressed = self.stdscr.getch()
		y,x = self.stdscr.getyx()
		if pressed == ENTER:
			# process the player selection
			pass
		elif pressed in DIRECTIONS:
			# move the cursor to a new position
			inc_x, inc_y = DIRECTIONS[pressed]
			x += inc_x
			y += inc_y
			
			# bound cursor
			if x > X_MAX: x = X_MAX
			if y > Y_MAX: y = Y_MAX
			if x < 0: x = 0
			if y < 0: y = 0

			# move cursor to the new position
			self.stdscr.move(y,x)


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

def get_board(c):
	ret=[]
	new_line ='-'*(2*BOARD_SIZE+1)
	ret.append(new_line)
	for x in range(BOARD_SIZE):
		new_line = "|"
		for y in range(BOARD_SIZE):
			new_line+=c+'|'
		ret.append(new_line)
        new_line ='-'*(2*BOARD_SIZE+1)
        ret.append(new_line)
	return ret

def main(stdscr):

	# clear screen
	stdscr.clear()
	
	# temporarily print a board
	write_board(stdscr, get_board('x'))

	# main game loop
	main_game = game(stdscr)
	while(True):
		main_game.player_turn()

	# await user input
	stdscr.getch()	

wrapper(main)
