import sys
import numpy
from collections import deque
from operator import itemgetter

EnglishLetterFrequencies = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.0095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.0074]
AlphabetSize = 26
AsciiOffset = 65

def main():
	if len(sys.argv) < 1:
		print('Please include some arguments.')
		return

	cipherText = ''
	if '-f' in sys.argv:
		if len(sys.argv) <= sys.argv.index('-f') + 1:
			print('Need an accompanying file name')
			return

		textFile = open(sys.argv[sys.argv.index('-f')+1])
		cipherText = textFile.read()
		textFile.close()

	if '-t' in sys.argv:
		if len(sys.argv) <= sys.argv.index('-t') + 1:
			print('Need ciper text')
			return

		cipherText = sys.argv[sys.argv.index('-t')+1]


	print(vigenereDecrypt(cipherText))

	perc = 0
	for n in EnglishLetterFrequencies:
		perc += n
	print(perc)

def vigenereCrackWithKeyLen(cipherText, keyLen):
	englishCorrelations = []
	shiftableEnglishFrequencies = deque(EnglishLetterFrequencies)

	for i in range(0, keyLen):
		textSubset = extractPositions(cipherText, i, keyLen)
		subsetFrequencies = countLetterFrequencies(textSubset)

		englishCorrelations.append(numpy.dot(shiftableEnglishFrequencies, subsetFrequencies))
		


def vigenereDecrypt(cipherText):
	likelyKeyLens = calculateLikelyKeyLens(cipherText)
	
	possibleSolutions = []

	for key in likelyKeyLens:
		possibleSolutions.append(vigenereCrackWithKeyLen(cipherText, key[0]))

	return likelyKeyLens


# Count collisions and return an ordered list of most likely lengths for the key
def calculateLikelyKeyLens(cipherText):
	coincidenceCounts = []
	shiftCipher = deque(cipherText)
	shiftCipher.rotate(1)

	for i in range(1, len(cipherText)):
		coincidenceCounts.append((i, countCoincidences(cipherText, shiftCipher)))
		shiftCipher.rotate(1)

	return sortKeys(coincidenceCounts)

def countCoincidences(coll1, coll2):
	if len(coll1) != len(coll2):
		raise InputError('Collections must have equal lengths to count coincidences')

	coinCount = 0
	for i in range(0, len(coll1)):
		if coll1[i] == coll2[i]:
			coinCount += 1

	return coinCount


def sortKeys(ls):
	sortedResults = sorted(ls, key=itemgetter(1), reverse=True)
	return sortedResults

def countLetterFrequencies(text):
	frequencies = []
	for i in range(0, AlphabetSize):
		frequencies.append(0)

	letterCount = len(text)
	for letter in text.upper():
		frequencies[ord(letter) - AsciiOffset] += 1

	return list(map(lambda x: x/5, frequencies))

def extractPositions(cipherText, i, keyLen):
	subCipher = []
	for i in range(i, len(cipherText), keyLen):
		subCipher.append(cipherText[i])
	return ''.join(subCipher)

if __name__ == "__main__":
	main()