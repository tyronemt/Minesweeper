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
from collections import defaultdict
import random


class Board:
	def __init__(self, row, col, totalMines, currentXY, cover = '.', bomb = 'B'):
		self.colDim = col
		self.rowDim = row
		self.totalMines = totalMines
		self.totalTiles = row * col
		self.cover = cover
		self.bomb = bomb
		self.__board = [[self.cover for i in range(self.colDim)] for j in range(self.rowDim)]
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


	def getTileAt(self, x, y):
		return self.__board[y][x]

	def incTileAt(self, x, y, val):
		self.__board[y][x] += val
	
	def decTileAt(self, x, y, val):
		self.__board[y][x] -= val

	def setTileAt(self, x, y, val):
		self.totalTiles -= 1
		if val < 0:
			self.totalMines -= 1
		self.__board[y][x] = val if val >=0 else self.bomb

	def iterAt(self, x, y, match = None):
		for row in [-1, 0, 1]:
			for col in [-1, 0, 1]:
				if not (row == col == 0)\
				and 0 <= x+col < self.colDim\
				and 0 <= y+row < self.rowDim:
					val = self.getTileAt(x+col, y+row)
					if match == None:
						yield x+col, y+row, val
					else:
						if match == val:
							yield x+col, y+row, val

	def iterBoard(self, match = None):
		for col in range(self.colDim):
			for row in range(self.rowDim):
				val = self.getTileAt(col, row)
				if match == None:
					yield col, row, val
				else:
					if match == val:
						yield col, row, val


	def isBombAt(self, x, y):
		return self.getTileAt(x,y) == self.bomb
	
	def isCoveredAt(self, x, y):
		return self.getTileAt(x,y) == self.cover





class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self.__board = Board(rowDimension, colDimension, totalMines, (startX, startY))
		self.__lastX = startX
		self.__lastY = startY
		self.__tileNumState = None
		self.__isGameOver = False
		self.__safeMoves = []
		self.__tocheck = []
		self.__flagCoor = set()
		self.__visited = set()
		self.__finishedMoves = set()
		self.__totalMines = totalMines
		
		
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################



	def getAction(self, number: int) -> "Action Object":
		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self.__tileNumState = number
		self.__updateGame()
		# print(self.__board)
		# print("Visited: ", self.__visited)
		# print("SafeMoves: ", self.__safeMoves)
		# print("flagCoor: ", self.__flagCoor)
		# print("Bombs ", self.__totalMines)
		# if (self.__board.totalMines + self.__totalMines == 0):				
		if not self.__isGameOver:
			self.__findSafeMoves(self.__lastX, self.__lastY)
			if (len(self.__safeMoves)):
				action = AI.Action.UNCOVER
				x, y = self.__getMove()
				self.__finishedMoves.add((x,y))
				return Action(action, x, y)

			self.__findBomb()
			if (len(self.__flagCoor)):
				action = AI.Action.FLAG
				x, y = self.__getMove()
				self.__visited.add((x, y))
				self.__finishedMoves.add((x,y))
				# self.__board.totalMines -= 1
				return Action(action, x, y)
			else:
				self.__lastX, self.__lastY = self.__getMoveProb()
				action = AI.Action.UNCOVER
				return Action(action, self.__lastX, self.__lastY)
				
		else:
			action = AI.Action.LEAVE
			return Action(action)

			
			

		# return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################







	#####################################################
	##		         ----------------				   ##
	##		         HELPER FUNCTIONS				   ##
	##		         ----------------				   ##
	#####################################################
	def __updateGame(self):
		if self.__tileNumState > 0:
			for x_temp, y_temp, val in self.__board.iterAt(self.__lastX, self.__lastY, match = self.__board.bomb):
				self.__tileNumState -= 1

		
		self.__board.setTileAt(self.__lastX, self.__lastY, self.__tileNumState)
		if self.__tileNumState > 0:									
				self.__tocheck.append((self.__lastX,self.__lastY))

		if self.__tileNumState < 0:
			self.subtract()

		if self.__board.totalTiles == 0:
			self.__isGameOver = True
		
		


	def __findSafeMoves(self, x, y):
		val = self.__board.getTileAt(x,y)
		if val == 0:
			for xTemp, yTemp, val in self.__board.iterAt(x, y, match = self.__board.cover):
				if (xTemp, yTemp) not in self.__safeMoves:
					self.__safeMoves.append((xTemp, yTemp))

		if (self.__board.totalMines == 0):	
			for x, y, val in self.__board.iterBoard(self.__board.cover):
				if (x,y) not in self.__safeMoves:
					self.__safeMoves.append((x,y))



	def __getMove(self):
		x = y = 0
		if (self.__safeMoves):
			x, y = self.__safeMoves.pop(0)
		elif(self.__flagCoor):
			x, y = self.__flagCoor.pop()
		self.__lastX = x
		self.__lastY = y
		return x, y
	

	def __findBomb(self):
		# self.__tocheck.sort(key= lambda coor: self.__board.getTileAt(coor[0], coor[1]))
		tempCopy = sorted(self.__tocheck, key= lambda coor: self.__board.getTileAt(coor[0], coor[1]))
		for temp in tempCopy[:]:
			wasBomb = self.__markBombs(temp)
			if wasBomb:
				self.__tocheck.remove(temp)
		

	def __markBombs(self, xy):
		x, y = xy
		tileNum = self.__board.getTileAt(x,y)
		emptyCoor = set()
		wasBomb = False
		for xTemp, yTemp, val in self.__board.iterAt(x, y, self.__board.cover):
			emptyCoor.add((xTemp, yTemp))

		if len(emptyCoor) == tileNum:
			wasBomb = True
			for coor in emptyCoor:
				if self.__board.getTileAt( coor[0], coor[1]) == self.__board.cover:
					self.__flagCoor.add(coor)
		return wasBomb

						
	def subtract(self):
		while (len(self.__visited)):
			coor = self.__visited.pop()
			for xTemp, yTemp, val in self.__board.iterAt(coor[0], coor[1]):
				if not self.__board.isBombAt(xTemp, yTemp) and not self.__board.isCoveredAt(xTemp,yTemp) :
					self.__board.decTileAt(xTemp, yTemp, 1)
					newVal = self.__board.getTileAt(xTemp,yTemp) 
					if newVal == 0:
						self.__findSafeMoves(xTemp, yTemp)
					else:
						self.__tocheck.append((xTemp, yTemp))




	def __getMoveProb(self):
		tempValues = defaultdict(lambda: 0.00) # {(x,y): probability}
		numberedTiles = set(self.__tocheck)
		if (numberedTiles): 
			while (len(numberedTiles)):
				x,y = numberedTiles.pop()
				count = 0 
				for tempX, tempY, tile in self.__board.iterAt(x,y, self.__board.cover):
					count += 1
				
				for tempX, tempY, tile in self.__board.iterAt(x,y, self.__board.cover):
					tempValues[(tempX, tempY)] += self.__board.getTileAt(x,y)/(count)

			tempList = tempValues.items()
			tempList = sorted(tempList, key = lambda x: x[1])

			smallest = tempList[0][1]
			anotherTempList = set()

			for ele in tempList:
				if ele[1] == smallest:
					anotherTempList.add(ele[0])
				else:
					break
			return anotherTempList.pop()


		else:
			# print(self.__board)
	
			for i in self.__board.iterBoard(self.__board.cover):
				return (i[0],i[1])
			
			# coveredTiles = [(x,y) for x,y, val in self.__board.iterBoard(self.__board.cover)]
			# return coveredTiles[random.randint(0, len(coveredTiles)-1)]
			
			# coveredTiles = set([(x,y) for x,y, val in self.__board.iterBoard(self.__board.cover)])
			# return (coveredTiles.pop())
	