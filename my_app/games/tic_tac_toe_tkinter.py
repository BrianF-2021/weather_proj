# python3 -m venv env/myenv
# source env/myenv/bin/activate
from tkinter import*
from tkinter import font as tkfont
from tkinter import messagebox
import time

# root = Tk()
# root.title("Tic-Tac-Toe")

isPlayerTurn = True
class T3:
	def __init__(self):
#		self.c = Canvas(root, width=1000, height=1300, bg="red")
#		self.c.place(relx=.02, rely=.02)
		self.root = Tk()
		# self.root.geometry("800x800")
		self.txt_font = tkfont.Font(weight=tkfont.BOLD)
		self.width = 14
		self.height = 10
		self.root.title("Tic-Tac-Toe")
		self.isPlayerTurn = True
		self.player = "X"
		self.ai = "O"
		self.isMax = True
		self.depth = 0
		self.state = NORMAL
#		self.usr_in = Entry(root)
#		self.usr_in.grid(row = 8, column = 0,columnspan = 3, padx = 50, pady = 10)

		self.bgColor = "lightgrey"

		self.btn1 = Button(self.root, bg=self.bgColor,text = " ",font = self.txt_font, width = self.width,height = self.height,  borderwidth= 4, command = lambda: self.clicked("btn1"))
		self.btn2 = Button(self.root, bg=self.bgColor,text = " ",font = self.txt_font,  width = self.width,height = self.height,  borderwidth= 4, command = lambda: self.clicked("btn2"))
		self.btn3 = Button(self.root, text = " ",font = self.txt_font, bg=self.bgColor, width = self.width,height = self.height,  borderwidth= 4, command = lambda: self.clicked("btn3"))

		self.btn4= Button(self.root, bg=self.bgColor,text = " ",font = self.txt_font,  width = self.width,height = self.height,  borderwidth= 4, command = lambda: self.clicked("btn4"))
		self.btn5 = Button(self.root, bg=self.bgColor,text = " ",font = self.txt_font,  width = self.width,height = self.height,  borderwidth= 4, command = lambda: self.clicked("btn5"))
		self.btn6 = Button(self.root, bg=self.bgColor,text = " ",font = self.txt_font,  width = self.width,height = self.height,  borderwidth= 4, command = lambda: self.clicked("btn6"))


		self.btn7= Button(self.root, bg=self.bgColor,text = " ",font = self.txt_font,  width = self.width,height = self.height,  borderwidth= 4, command = lambda: self.clicked("btn7"))
		self.btn8 = Button(self.root, bg=self.bgColor,text = " ",font = self.txt_font,  width = self.width,height = self.height,  borderwidth= 4, command = lambda: self.clicked("btn8"))
		self.btn9 = Button(self.root, bg=self.bgColor,text = " ",font = self.txt_font,  width = self.width,height = self.height,  borderwidth= 4, command = lambda: self.clicked("btn9"))

		self.btnReset = Button(self.root, bg="lightgreen",text = "Reset",font = self.txt_font, width = 39, height = 8,  borderwidth=4, command = lambda: self.reset())

		#create grid
		self.btn1.grid(row = 0, column = 0)
		self.btn2.grid(row = 0, column = 1)
		self.btn3.grid(row = 0, column = 2)

		self.btn4.grid(row = 1, column = 0)
		self.btn5.grid(row = 1, column = 1)
		self.btn6.grid(row = 1, column = 2)

		self.btn7.grid(row = 2, column = 0)
		self.btn8.grid(row = 2, column = 1)
		self.btn9.grid(row = 2, column = 2)

		self.btnReset.grid(row = 4, column =0, columnspan = 3)
#		self.btnReset.place(relx=0.5, rely=0.5, anchor=CENTER)

		self.board = [
		[self.btn1, self.btn2, self.btn3],
		[self.btn4, self.btn5, self.btn6],
		[self.btn7, self.btn8, self.btn9]]

		self.miniMaxBoard =[
				[".",".","."],
				[".", ".","."],
				[".",".","."]]


#	def clear(self):
#		return self.usr_in.delete(0, END)


	def buttonsState(self):
		self.btn1.config(state = self.state)
		self.btn2.config(state =  self.state)
		self.btn3.config(state =  self.state)
		self.btn4.config(state =  self.state)
		self.btn5.config(state =  self.state)
		self.btn6.config(state =  self.state)
		self.btn7.config(state =  self.state)
		self.btn8.config(state =  self.state)
		self.btn9.config(state =  self.state)

#		self.canvas.create_window(10, 10, anchor=S, window=self.btn1)

	def isBoardFull(self):
		for i in range(3):
			for j in range(3):
				if self.miniMaxBoard[i][j]== ".":
					return False
		return True


	def ifBoardIsFull(self):
		if self.isBoardFull():
			messagebox.showinfo("TIE", "*** TIE ***")
			self.state = DISABLED
			self.buttonsState()
			return
		return


	def reset(self):
		self.state = NORMAL
		self.buttonsState()
		self.isPlayerTurn=True
#		self.clear()
		for i in range(3):
			for j in range(3):
				self.board[i][j]["text"] = " "
				self.miniMaxBoard[i][j] = "."


	def getMove(self, btn):
		position ={
		"btn1": (0,0),
		"btn2": (0,1),
		"btn3": (0,2),
		"btn4": (1,0),
		"btn5": (1,1),
		"btn6": (1,2),
		"btn7": (2,0),
		"btn8": (2,1),
		"btn9": (2,2)}

		pos = position.get(btn)
		return pos


	def isWin(self, player):

		#Vertical
		if all([player == self.miniMaxBoard[i][0] for i in range(3)]) or all([player == self.miniMaxBoard[i][1] for i in range(3)]) or all([player == self.miniMaxBoard[i][2] for i in range(3)]):
			return True

		#Horizontal
		if all([player == self.miniMaxBoard[0][i] for i in range(3)]) or all([player == self.miniMaxBoard[1][i] for i in range(3)]) or all([player == self.miniMaxBoard[2][i] for i in range(3)]):
			return True

		#diagb
		if all([player == self.miniMaxBoard[i][i] for i in range(3)]):
			return True

		#diagf
		if all([player == self.miniMaxBoard[i][-(i+1)] for i in range(3)]):
			return True
		return False


	def isValidMove(self, pos):
		r,c = pos
		if self.miniMaxBoard[r][c] in [self.player, self.ai]:
			return False
		return True


	def boardState(self):
		if self.isWin(self.player):
	#			dic["score"]= 10
			score = 10
			return score
		elif self.isWin(self.ai):
	#			dic["score"] = -10
			score = -10
			return score
		else:
			score = 0
	#			dic["score"] = 0
			return score


	def miniMax(self, isMax, depth):
		# ai is Min
		# player is Max
#		self.usr_in.insert(0, str(depth))
#		time.sleep(.5)
		score = self.boardState()
		if score == 10:
			return score - depth
		if score == -10:
			return score + depth
		if self.isBoardFull():
			return 0

		if isMax:
			best  = -1000000
			for i in range(3):
				for j in range(3):
					if self.isValidMove((i,j)):
						self.miniMaxBoard[i][j]= self.player
						best = max(self.miniMax(not isMax, depth+1), best)
						self.miniMaxBoard[i][j]= "."
			return best

		else:
			best = 1000000
			for i in range(3):
				for j in range(3):
					if self.isValidMove((i,j)):
						self.miniMaxBoard[i][j]= self.ai
						best=min(self.miniMax(not isMax, depth+1), best)
						self.miniMaxBoard[i][j] = "."
			return best


	def findBestMove(self):
		bestMove = (-1,-1)
		bestVal = 1000000
		for i in range(3):
			for j in range(3):
				if self.miniMaxBoard[i][j] == ".":
					self.miniMaxBoard[i][j] = self.ai
					moveVal= self.miniMax(self.isMax, 0)
#					self.usr_in.insert(0, #str(moveVal)+";"+str(i)+str(j)+".")
#					time.sleep(.5)
	#				print(moveVal)
					self.miniMaxBoard[i][j] = "."
					if (moveVal <= bestVal):
						bestMove = (i, j)
						bestVal = moveVal
	#					print(bestVal)
		return bestMove


	def clicked(self, btn):
		r,c = self.getMove(btn)
		if (self.miniMaxBoard[r][c] == ".") and (self.board[r][c]["text"] == " ") and self.isPlayerTurn:
#			self.usr_in.insert(0, str(r)+str(c))
			self.miniMaxBoard[r][c] = self.player
			self.board[r][c]["text"] = self.player
			self.isPlayerTurn = False
			if self.isWin(self.player):
				messagebox.showinfo("win", "*** PLAYER_1 WINS ***")
				self.state = DISABLED
				self.buttonsState()

		if not self.isPlayerTurn:
			r,c = self.findBestMove()
#			self.usr_in.insert(0, str(r)+str(c))
			self.miniMaxBoard[r][c] = self.ai
			self.board[r][c]["text"] = self.ai
			self.isPlayerTurn = True
			if self.isWin(self.ai):
				messagebox.showinfo("win", "*** AI WINS ***")
				self.state = DISABLED
				self.buttonsState()
			self.ifBoardIsFull()


def tictactoe():
	game = T3()
	messagebox.showinfo("PLAYERS", "PLAYER_1:  X\nAI:  O")
	game.root.mainloop()

