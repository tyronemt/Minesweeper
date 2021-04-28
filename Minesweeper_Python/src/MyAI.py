# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================
from AI import AI
from Action import Action

class Board:
	def __init__(self, arr, currentXY):
		self.__board = arr
		self.size = len(arr)
		self.x, self.y  = currentXY

	
	def __getitem__(self,key):
		return self.__board[key]

	def __iter__(self):
		return iter(self.__board)
	
	def __str__(self):
		s = "\n"
		for row in self.__board[::-1]:
			temp = [str(i)  for i in row[:]]
			s += '  '.join(temp)
			s += '\n'
		return s



class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		
		# Test by using:
		#		py main.py -d
		self.__rowDim = rowDimension
		self.__colDim = colDimension
		self.__totalTiles = rowDimension * colDimension
		self._uncensored = "."

		# self.__board = [['N' for i in range(self.__colDim)] for j in range(self.__rowDim)]  # Not sure whether to keep this
		self.__board = Board([[ self._uncensored for i in range(self.__colDim)] for j in range(self.__rowDim)], (startX, startY))
		self.__lastX = startX
		self.__lastY = startY
		self.__totalMines = totalMines
		self.__tileNumState = None
		self.__isGameOver = False
		self.__safeMoves = []
		self.__tocheck = []
		self.__flagCoor = []
		self.__visited = []
		
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################



	def getAction(self, number: int) -> "Action Object":
		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self.__tileNumState = number
		self.__updateGame()
		if not self.__isGameOver:
			self.__findSafeMoves()
			if (len(self.__safeMoves) != 0):
				
				action = AI.Action.UNCOVER
				x, y = self.__getMove()
				return Action(action, x, y)
			else:
				self.__findBomb()
				if (len(self.__flagCoor) != 0):
					action = AI.Action.FLAG
					x, y = self.__getMove()
					self.__visited.append((x, y))
					return Action(action, x, y)
				else:
					self.subtract()

				
				
			
			
		else:
			action = AI.Action.LEAVE
			return Action(action)

			
			


		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################







	#####################################################
	##		         ----------------				   ##
	##		         HELPER FUNCTIONS				   ##
	##		         ----------------				   ##
	#####################################################
	def __updateGame(self):
		if self.__tileNumState == -1:
			self.__tileNumState = 'B'
		self.__board[self.__lastY][self.__lastX] = self.__tileNumState
		if self.__tileNumState != 'B' and self.__tileNumState > 0:
				self.__tocheck.append(((self.__lastX,self.__lastY), self.__tileNumState))
		self.__totalTiles -= 1
		if self.__totalMines == self.__totalTiles:
			self.__isGameOver == True



	def __getTileAt(self, x, y):
		val = self.__board[y][x]
		return None if val  == self._uncensored else val

	def __findSafeMoves(self):
		if self.__tileNumState == 0:
			x = self.__lastX
			y = self.__lastY
			for i in [-1, 0, 1]:
				for j in [-1, 0, 1]:
					if not (i == j == 0 )\
					 and 0 <= x+i < self.__rowDim\
					 and 0 <= y+j < self.__colDim\
					 and self.__getTileAt(x+i, y+j) == None \
					 and (x+i, y+j) not in self.__safeMoves:
						self.__safeMoves.append((x+i, y+j))

	def __getMove(self):
		x = y = 0
		if (self.__safeMoves):
			x, y = self.__safeMoves.pop(0)
		elif(self.__flagCoor):
			x, y = self.__flagCoor.pop(0)
		self.__lastX = x
		self.__lastY = y
		return x, y
	
	def __findBomb(self):
		self.__tocheck.sort(key= lambda x: x[1])
		
		while (len(self.__tocheck) != 0):
			temp = self.__tocheck.pop(0) # ((self.__lastX,self.__lastY), self.__tileNumState)
			tile_int = temp[1]
			
			temp_board = self.__makeTempBoard(temp[0][0], temp[0][1]) #X and Y start at 0
			number_of_bombs = self.__countBombs(temp_board)
			if tile_int == number_of_bombs:
				self.__bomb_corr(temp_board, (temp[0][0], temp[0][1]))
			



			
	def __bomb_corr(self, temp_board, middle):
		bombs = []
		for row in [-1, 0, 1]:
			for col in [-1, 0 , 1]:
				if (0 <= 1 + row < temp_board.size and  0 <=  1 + col < len(temp_board[0])):
					if ((temp_board[1 + row][1 + col]) == self._uncensored):
						if ((middle[0] + col, middle[1] + row) not in self.__flagCoor):
							self.__flagCoor.append((middle[0] + col, middle[1] + row))

						
	def subtract(self):
		while (self.__visited):
			coor = self.__visited.pop(0)
			temp = self.__makeTempBoard(coor[0],coor[1])
			for row in [-1, 0, 1]:
				for col in [-1, 0 , 1]:
					if (0 <= 1 + row < temp.size and  0 <=  1 + col < len(temp[0])):
						if (temp[1 + row][1 + col] not in [self._uncensored, "B", "E", 0]):
							self.__board[coor[1] + row][coor[0] + col] -= 1
							if (self.__board[coor[1] + row][coor[0] + col] == 0):
								self.__safeMoves.append((coor[0] + col,coor[1] + row))


						


	def __countBombs(self, temp_board):
		count = 0
		for row in temp_board:
			for col in row:
				if col == self._uncensored:
					count += 1
		return count
			


		# Go through each tile and check if the number of uncover tiles in its grid = its tile number
		# if so the remaining tiles are bombs and should be flagged
		# save all the flag x,y coor
		
		
		
				



		
	def __makeTempBoard(self, x,y):
		temp = [] 
		for row in [-1, 0, 1]:
			tempRow = []
			for col in [-1, 0 , 1]:
				if 0 <= x+col < self.__rowDim and 0 <= y+row < self.__colDim:
					tempRow.append(self.__board[y+row][x+col])
				else:
					tempRow.append('E')
			temp.append(tempRow)
		tempBoard = Board(temp, (x,y))
		return tempBoard
				
		


