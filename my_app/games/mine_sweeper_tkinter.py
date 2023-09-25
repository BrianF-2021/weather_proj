from tkinter import*
from tkinter import messagebox
import time
import random
from collections import deque
import math

#root = Tk()
# class Level():

# 	def __init__(self):
# 		self.level = .1
# 		self.size_r = 12
# 		self.size_c = 12

# 	def change_level(self, lvl):
# 		#height/number of rows
# 		#self.size_r = 12
# 		#width/number of columns
# 		#self.size_c = 12
# 		if lvl == "Easy":
# 			self.size_r = 12
# 			self.size_c = 12
# 			self.lvl = .1

# 		if lvl == "Med":
# 			#324sq @ 40bombs
# 			self.size_r = 18
# 			self.size_c = 18
# 			self.lvl = .15

# 		if lvl == "Hard":
# 			#625sq @ 78bombs
# 			self.size_r = 25
# 			self.size_c = 25
# 			self.lvl = .2

# 		return (self.lvl, self.size_r, self.size_c)





class Mine_Sweeper():
	def __init__(self):
		self.root = Tk()
		self.root.title("Mine Sweeper")
		# self.difficulty = 2
		self.lvl = .1
		#height/number of rows
		self.size_r = 12
		#width/number of columns
		self.size_c = 12
		self.grid =[]
		self.board = []
		self.w = 1
		self.h = 1
		self.visited =[]
		self.played_square_count = 0
		self.bomb_count = 0
		self.game_over = False
		self.flagging = False
		self.flag_count = 0
		self.square_count = self.size_r*self.size_c
		self.btn = Button(self.root, text = " ")
		self.default_btn_color= self.btn["bg"]
		self.default_foreground = self.btn["foreground"]
		self.bgColor = "lightgreen"
		self.btn_color = "GREY"
		self.lbl = None
#		self.usr_in = Entry(self.root)
#		self.usr_in.grid(row = self.size_r+3, column = 0,columnspan = 5, padx = 75, pady = 20)
#		self.usr_in.delete(0, END)

	def create_taskbar(self):
		taskwidth = self.root.winfo_screenwidth()
#		taskheight = self.root.winfo_screenheight()
		taskbar = Canvas(self.root, height = 150,width = taskwidth, bg = "skyblue", highlightthickness = 0)
#		taskbar.grid(row = self.size_r, column = 5)
		taskbar.place(x=0, y=0)
#		Port.place(relx = 0.5, rely = 0.995, anchor = "center")




	def create_game(self, l=.1, r=12, c=12):
		self.size_r = r
		self.size_c = c
		self.lvl = l
#		self.create_taskbar()
		board_row = []
		grid_row =[]
		square = 0
		for i in range(0,self.size_r):
			for j in range(0,self.size_c):
				square += 1
				place = Button(self.root, text = " ", width = self.w ,height = self.h,  borderwidth= 4, command = lambda r=i, c=j: self.clicked(r,c))
				board_row.append(" ")
				place.grid(row = i, column = j)
				grid_row.append(place)
			self.grid.append(grid_row)
			self.board.append(board_row)
			board_row=[]
			grid_row = []
		self.create_buttons()


	def create_buttons(self):
		reset = Button(self.root,bg=self.bgColor, font=('calibri', 9, 'bold'), text = "Reset", width = self.w+4, height = self.h+1,  borderwidth=4, command = lambda: self.reset())
		reset.grid(row = self.size_r, column =0, columnspan = 2)

		self.flag = Button(self.root, bg=self.bgColor,text = "Flag", font=('calibri', 9, 'bold'), width = self.w+4, height = self.h+1,  borderwidth=4, command = lambda: self.isflagging())
		self.flag.grid(row = self.size_r, column =2, columnspan = 2)

		self.lbl = Label(self.root, width = 15,height = 3, font=('calibri', 9, 'bold'), background = "yellow", text = "")
		self.lbl.grid(row = self.size_r, column = 4, columnspan = 3)
		self.place_bombs()
		self.number_squares()
		self.lbl["text"] = "Bombs: "+str(self.flag_count)

		##options = ["Easy", "Med","Hard"]
# datatype of menu text
		##self.level = StringVar()
# initial menu text
		##self.level.set("Easy")
# Create Dropdown menu
		##drop = OptionMenu( self.root, self.level , *options )
#		self.change_level(self.level.get())
		# self.level.get()
		##drop.grid(row = self.size_r, column = 6, columnspan =2)
#		self.usr_in.insert(0, "Bombs: "+str(self.flag_count))


	def change_level(self, lvl):
		#height/number of rows
		#self.size_r = 12
		#width/number of columns
		#self.size_c = 12
		if lvl == "Easy":
			self.size_r = 12
			self.size_c = 12
			self.lvl = .1

		if lvl == "Med":
			#324sq @ 40bombs
			self.size_r = 18
			self.size_c = 18
			self.lvl = .15

		if lvl == "Hard":
			#625sq @ 78bombs
			self.size_r = 25
			self.size_c = 25
			self.lvl = .2

		return self.set_level(self.lvl, self.size_r, self.size_c)

	def place_bombs(self):
		self.bomb_count = math.floor(self.square_count*self.lvl)
		self.flag_count = self.bomb_count
		for i in range(self.bomb_count):
			y = random.randint(0, self.size_c-1)
			x = random.randint(0, self.size_r-1)
			while self.board[x][y] == "¤":
				y = random.randint(0, self.size_c-1)
				x = random.randint(0, self.size_r-1)
			self.board[x][y] = "¤"
		return


	def place_count(self, x, y):
		if self.board[x][y] == "¤":
			return
		count = 0
		moves = self.get_next_moves((x,y))
		for move in moves:
			r,c = move
			if self.is_pos_onboard(r,c):
				if self.board[r][c] == "¤":
					count += 1
		if count > 0:
			self.board[x][y] = count
#			self.usr_in.insert(0, "count: "+str(count))
		return


	def number_squares(self):
		for x in range(self.size_r):
			for y in range(self.size_c):
				self.place_count(x,y)


	def reveal_board(self):
		for i in range(self.size_r):
			for j in range(self.size_c):
				self.grid[i][j]["text"] = self.board[i][j]
				self.grid[i][j].config(state = DISABLED)



	def is_pos_onboard(self, x,y):
		if (x<0) or (x>= self.size_r)or (y<0) or (y >=self.size_c):
			return False
		return True


	def get_next_moves(self, pos):
		x,y = pos
		u =  (x, y+1)
		l = (x-1, y)
		d = (x, y-1)
		r = (x+1, y)
		ur = (x+1, y+1)
		dr = (x+1, y-1)
		ul = (x-1, y+1)
		dl = (x-1, y-1)
		moves = (u, ur, r, dr, d, dl, l, ul)
		return moves



	def nextValidMoves(self, pos):
		validmoves =[]
		moves = self.get_next_moves(pos)
		for i in moves:
			x,y = i
			if self.is_pos_onboard(x,y):
				validmoves.append(i)
		return validmoves


#	def clear(self):
#		return self.usr_in.delete(0, END)

	def set_level(self, level, row, col):
		self.visited = []
		self.board = []
		self.grid = []
		self.create_game(level, row, col)

	def reset(self):
#		self.clear()
		self.visited = []
		self.board = []
		self.grid = []
		self.create_game()


	def isWin(self):
		self.played_square_count = 0
		for i in range(self.size_r):
			for j in range(self.size_c):
				if  (self.grid[i][j]["bg"] == self.btn_color) or (self.grid[i][j]["text"] == "F"):
					self.played_square_count += 1
		if self.played_square_count == self.square_count:
			return True
		return False


	def update_grid(self):
		self.lbl["text"] = "Bombs: "+str(self.flag_count)
#		self.clear()
#		self.usr_in.insert(0, "Bombs: "+str(self.flag_count))
		for i in self.visited:
			r,c = i
			board_value = self.board[r][c]
			grid_value = self.grid[r][c]["text"]
#			self.usr_in.insert(0, "blanks: "+str(r)+str(c))
			if board_value == " " and grid_value == " " :
				self.grid[r][c].config(state = DISABLED)
			if grid_value != "F":
				self.grid[r][c]["bg"] = self.btn_color
				self.grid[r][c]["text"] = board_value


	def isflagging(self):
		if self.flagging:
			self.flag["bg"] = self.bgColor
			# self.flag["bg"] = self.default_btn_color
			self.flagging = False

			return
		else:
			self.flag["bg"] = "red"
			self.flagging = True
			return


	def clicked(self, x,y):
		board_value = self.board[x][y]
		grid_value = self.grid[x][y]["text"]
#		self.usr_in.insert(0, "pos: "+x+y)
		if self.flagging :
			if grid_value == "F":
				self.grid[x][y]["foreground"] = self.default_foreground
				self.grid[x][y]["text"] = " "
				self.flag_count += 1
				self.lbl["text"] = "Bombs: "+str(self.flag_count)
#				self.clear()
#				self.usr_in.insert(0, "Bombs: "+str(self.flag_count))
			elif grid_value == " ":
				self.grid[x][y]["foreground"] = "red"
				self.grid[x][y]["text"] = "F"
				self.flag_count -=1
				self.lbl["text"] = "Bombs: "+str(self.flag_count)
			if self.isWin():
				answer = messagebox.askyesno("Mine Sweeper", "** YOU WIN **\n\n     PLAY AGAIN?")
#				self.clear()
#				self.usr_in.insert(0, "Bombs: "+str(self.flag_count))
		else:
			if grid_value != "F":
				if board_value == " ":
					self.bfs(x,y)
				if board_value == "¤":
					self.reveal_board()
					answer = messagebox.askyesno("Mine Sweeper", "** BETTER LUCK NEXT TIME **\n\n         PLAY AGAIN?")
					if answer:
						self.reset()
					else:
						self.root.destroy()
						return
				if board_value not in [" ", "¤"]:
					if (x,y) not in self.visited:
						self.visited.append((x,y))
					self.grid[x][y]["text"] = self.board[x][y]
			self.update_grid()
			if self.isWin():
				answer = messagebox.askyesno("Mine Sweeper", "** YOU WIN **\n\n     PLAY AGAIN?")
				if answer:
					self.reset()
				else:
					self.root.destroy()


	def bfs(self, r,c):
		if (r,c) not in self.visited:
			self.visited.append((r,c))
		coords = self.nextValidMoves((r,c))
		for coord in coords:
			x,y = coord
			value = self.board[x][y]
			if value not in [" ", "¤"]:
				self.visited.append((x,y))
			if coord not in self.visited and value == " ":
				self.visited.append((x,y))
				self.bfs(x,y)
		return



def mine_sweeper():
	ms = Mine_Sweeper()
	ms.create_game()
	# messagebox.showinfo("Mine Sweeper", "Let's Play Mine Sweeper!\n\n     Good Luck!")
	ms.root.mainloop()
