
Letters = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'

class PlayfairGrid:
	Dimensions = [5, 5]
	keyword = None
	grid = [[0 for x in range(5)] for x in range(5)]

	def __init__(self, keyword):
		keyword = keyword.upper()
		self.keyword = keyword

		row = 0
		col = 0
		for i in range(len(keyword)):
			letter = keyword[i]
			if not self.contains(letter):
				self.grid[col][row] = letter
				col += 1
				col %= 5
				if col == 0:
					row += 1

		missingLetters = self.getMissingLetters()

		for letter in missingLetters:
			self.grid[col][row] = letter
			col += 1
			col %= 5
			if col == 0:
				row += 1

	def decodeDigraph(self, digraph):
		digraph = digraph.upper()
		digraph.replace("J", "I")

		if digraph[0] == digraph[1]:
			print("duplicate letter")
			raise Exception
		
		for l in digraph:
			if not self.contains(l):
				print("Error with digraph")
				raise Exception

		firstLetter = self.find(digraph[0])
		secLetter = self.find(digraph[1])

		result = ''

		if firstLetter[0] == secLetter[0]:
			# letters on the same col
			l1 = self.getAt((firstLetter[0], (firstLetter[1] - 1) % 5))
			l2 = self.getAt((secLetter[0], (secLetter[1] - 1) % 5))
			result += l1 + l2

		elif firstLetter[1] == secLetter[1]:
			l1 = self.getAt(((firstLetter[0] - 1) % 5, firstLetter[1]))
			l2 = self.getAt(((secLetter[0] - 1) % 5, secLetter[1]))
			result += l1 + l2

		else:
			l1 = self.getAt((secLetter[0], firstLetter[1]))
			l2 = self.getAt((firstLetter[0], secLetter[1]))
			result += l1 + l2

		return result

	def encodeDigraph(self, digraph):
		digraph = digraph.upper()
		digraph.replace("J", "I")

		if digraph[0] == digraph[1]:
			print("duplicate letter")
			raise Exception
		
		for l in digraph:
			if not self.contains(l):
				print("Error with digraph")
				raise Exception

		firstLetter = self.find(digraph[0])
		secLetter = self.find(digraph[1])

		result = ''

		if firstLetter[0] == secLetter[0]:
			# letters on the same col
			l1 = self.getAt((firstLetter[0], (firstLetter[1] + 1) % 5))
			l2 = self.getAt((secLetter[0], (secLetter[1] + 1) % 5))
			result += l1 + l2

		elif firstLetter[1] == secLetter[1]:
			l1 = self.getAt(((firstLetter[0] + 1) % 5, firstLetter[1]))
			l2 = self.getAt(((secLetter[0]+1) % 5, secLetter[1]))
			result += l1 + l2

		else:
			l1 = self.getAt((secLetter[0], firstLetter[1]))
			l2 = self.getAt((firstLetter[0], secLetter[1]))
			result += l1 + l2

		return result

	def getAt(self, indices):
		return self.grid[indices[0]][indices[1]]


	def find(self, symbol):
		for row in range(self.Dimensions[1]):
			for col in range(self.Dimensions[0]):
				if str(symbol).upper() == str(self.grid[col][row]).upper():
					return (col, row)
		return (-1, -1)


	def getMissingLetters(self):
		missingLetters = []
		for letter in Letters:
			if not self.contains(letter):
				missingLetters.append(letter)

		return missingLetters

	def printGrid(self, outstream=None):
		print("----------", file=outstream)
		for row in range(self.Dimensions[1]):
			print("|", file=outstream, end="")
			for col in range(self.Dimensions[0]):
				print(self.grid[col][row] + "|", file=outstream, end="")
			print("", file=outstream)
		print("----------", file=outstream)

	def contains(self, symbol):
		for sublist in self.grid:
			for sym in sublist:
				if str(sym).upper() == str(symbol).upper():
					return True
		return False
