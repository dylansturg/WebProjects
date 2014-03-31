class AdfgxKey:
	keyword = None
	textGrid = None
	shuffledGrid = None

	def __init__(self, keyword):
		self.keyword = keyword


	def buildTextGrid(self, cipherText, keyorder=None):
		if not keyorder:
			keyorder = self.keyword

		self.textGrid = [(x, []) for x in self.keyword]
		colCount = len(self.keyword)
		col = 0
		overlap = len(cipherText) % len(self.keyword)
		for i in range(len(cipherText)):
			remaining = len(cipherText) - i - 1
			if overlap > 0 and remaining < overlap:
				shiftCol = self.findColumn(keyorder[col])
				self.textGrid[shiftCol][1].append(cipherText[i])
			else:
				self.textGrid[col][1].append(cipherText[i])
			col += 1
			col %= colCount

	def findColumn(self, letter):
		for i in range(len(self.textGrid)):
			if self.textGrid[i][0] == letter:
				return i

	def encryptMessage(self, cipherText, key=None):
		self.buildTextGrid(cipherText, keyorder=key)
		self.shuffleCipherText(shuffleKey=key)
		return self.getShuffledText()

	def shuffleCipherText(self, shuffleKey=None):
		if not shuffleKey:
			shuffleKey = alphabetizeLetters(self.keyword)

		for letter in shuffleKey:
			if letter not in self.keyword:
				raise ValueError("%s not in keyword (%s)" % (letter, self.keyword))

		shuffledGrid = [(x, []) for x in shuffleKey]

		for col in shuffledGrid:
			originalCol = self.keyword.find(col[0])
			col[1].extend(self.textGrid[originalCol][1])

		self.shuffledGrid = shuffledGrid

	def getShuffledText(self):
		maxRow = 0
		for col in self.shuffledGrid:
			if len(col[1]) > maxRow:
				maxRow = len(col[1])

		row = 0
		result = ''
		while(row < maxRow):
			for col in self.shuffledGrid:
				result += safe_get(col[1], row, default='')
			row += 1
		return result
		
	@staticmethod
	def printGrid(grid):
		maxRow = 0
		print("|", end="")
		for col in grid:
			print(col[0], end="|")
			if len(col[1]) > maxRow:
				maxRow = len(col[1])
		print("")
		print("--------")
		row = 0

		while(row < maxRow):
			print("|", end="")
			for col in grid:
				print(safe_get(col[1], row), end="|")
			row += 1
			print("")
			print("--------")

	def printShuffledGrid(self):
		AdfgxKey.printGrid(self.shuffledGrid)

	def printTextGrid(self):
		AdfgxKey.printGrid(self.textGrid)

def alphabetizeLetters(letters):
	return ''.join(sorted(list(letters)))

def safe_get(ls, index, default=' '):
	try:
		return ls[index]
	except IndexError:
		return default
