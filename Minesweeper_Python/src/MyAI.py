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

		self.__board = [['N' for i in range(self.__colDim)] for j in range(self.__rowDim)]  # Not sure whether to keep this
		self.__lastX = startX
		self.__lastY = startY
		self.__totalMines = totalMines
		self.__tileNumState = None
		self.__isGameOver = False
		self.__safeMoves = []
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################



	def getAction(self, number: int) -> "Action Object":
		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self.__tileNumState = number
		self.__updateGame()
		self.__findSafeMoves()
		if not self.__isGameOver:
			action = AI.Action.UNCOVER
			x, y = self.__getMove()
			self.__printBoard()
			return Action(action, x, y)
		else:
			action = AI.Action.LEAVE
			return Action(action)

			
			


		print(number)
		input("Cont...")
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
		self.__board[self.__lastY][self.__lastX] = self.__tileNumState
		self.__totalTiles -= 1
		if self.__totalMines == self.__totalTiles:
			self.__isGameOver == True


	def __printBoard(self):
		''' 
		For debugging purposes I guess
		It works now
		'''
		print()
		for row in self.__board[::-1]:
			temp = [str(i) for i in row[:]]
			print('  '.join(temp))
		print()


	def __getTileAt(self, x, y):
		'''
		Index starts at 1 just to stay consistent with the handling of indexing
		'''
		val = self.__board[y][x]
		return None if val  == 'N' else val


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
		if len(self.__safeMoves) :
			x, y = self.__safeMoves.pop(0)
		self.__lastX = x
		self.__lastY = y
		
		return x, y



		
