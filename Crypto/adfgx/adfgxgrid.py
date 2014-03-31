from ciphertext import CipherText

GridLetterMap = ['A', 'D', 'F', 'G', 'X']
class AdfgxGrid:
	Dimensions = [5, 5]
	grid = [[0 for x in range(5)] for x in range(5)]


	def __init__(self, alphabet, duplicate=('i', 'j')):
		alphabetSize = len(alphabet)
		row, col = 0, 0
		for letter in alphabet:
			self.grid[col][row] = letter
			col += 1
			col %= 5
			if col == 0:
				row += 1

	def find(self, letter):
		for row in range(self.Dimensions[1]):
			for col in range(self.Dimensions[0]):
				if self.grid[col][row].upper() == letter.upper():
					return (row, col)
		return None

	def encodeMessage(self, message):
		result = ''
		for letter in message:
			result += self.encode(letter)
		return result

	def decodeMessage(self, cipherText):
		result = ''
		for pair in CipherText(cipherText).generatePairs():
			result += self.decode(pair)
		return result

	def encode(self, letter):
		location = self.find(letter)
		return GridLetterMap[location[0]] + GridLetterMap[location[1]]

	def decode(self, digraph):
		location = (safe_index(GridLetterMap, digraph[0]), safe_index(GridLetterMap, digraph[1]))

		if -1 in location:
			raise ValueError("Bad digraph: %s" % digraph)

		return self.grid[location[1]][location[0]]

	def printGrid(self, outstream=None):
		print("----------", file=outstream)
		for row in range(self.Dimensions[1]):
			print("|", file=outstream, end="")
			for col in range(self.Dimensions[0]):
				print(self.grid[col][row] + "|", file=outstream, end="")
			print("", file=outstream)
		print("----------", file=outstream)

def safe_index(ls, item, default=-1):
	try:
		return ls.index(item)
	except ValueError:
		return default