from ciphertext import CipherText
from collections import deque
from operator import itemgetter
import numpy

EnglishLetterFrequencies = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.0095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.0074]
AlphabetSize = 26
Letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class VigenereKeySolver:
	keyLengths = []
	cipherText = CipherText('')

	def __init__(self, cipherText, keylens):
		self.keyLengths = keylens
		self.cipherText = cipherText

	def calculatePotentialKey(self):

		keyLen = next(self.keyLengths)

		englishCorrelations = []

		for i in range(0, keyLen):
			shiftableEnglishFrequencies = deque(EnglishLetterFrequencies)
			textSubset = self.cipherText.substringByIncrement(i, keyLen)
			subsetFrequencies = textSubset.countLetterFrequencies(AlphabetSize)
			englishCorrelations.append([])

			for j in range(0, AlphabetSize):
				englishCorrelations[i].append((numpy.dot(shiftableEnglishFrequencies, subsetFrequencies), j))
				shiftableEnglishFrequencies.rotate(1)

		for i in range(0, len(englishCorrelations)):
			englishCorrelations[i] = sorted(englishCorrelations[i], key=itemgetter(0), reverse=True)

		keyInts = []
		for k in englishCorrelations:
			keyInts.append(k[0][1])

		key = ''
		for i in keyInts:
			key += Letters[i]

		yield key

class VigenereKeyLengthSolver:
	cipherText = CipherText()
	potentialKeyLengths = []

	def __init__(self, cipherText):
		self.cipherText = cipherText

	def generateKeyLengths(self):
		if len(self.potentialKeyLengths) <= 0:
			self.calculateLikelyKeyLens()

		for l in self.potentialKeyLengths:
			yield l[0]

	def calculateLikelyKeyLens(self):
		coincidenceCounts = []
		shiftCipher = deque(self.cipherText)
		shiftCipher.rotate(1)

		for i in range(1, len(self.cipherText)):
			coincidenceCounts.append((i, self.countCoincidences(i)))
			shiftCipher.rotate(1)

		self.potentialKeyLengths = sorted(coincidenceCounts, key=itemgetter(1), reverse=True)
		return True

	def countCoincidences(self, offset):
		coinCount = 0
		for i in range(0, len(self.cipherText)-offset):
			if self.cipherText[i] == self.cipherText[i+offset]:
				coinCount += 1

		return coinCount