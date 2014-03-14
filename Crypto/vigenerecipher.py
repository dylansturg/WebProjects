import sys
import numpy
from collections import deque
from operator import itemgetter

EnglishLetterFrequencies = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.0095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.0074]
AlphabetSize = 26
AsciiOffset = 65
Letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

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


def calculatePotentialKey(cipherText, keyLen):
	englishCorrelations = []

	for i in range(0, keyLen):
		shiftableEnglishFrequencies = deque(EnglishLetterFrequencies)
		textSubset = extractPositions(cipherText, i, keyLen)
		subsetFrequencies = countLetterFrequencies(textSubset)
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

	return key

def vigenereDecrypt(cipherText):
	likelyKeyLens = calculateLikelyKeyLens(cipherText)
	
	possibleSolutions = []

	print('Trying key length: %s' % likelyKeyLens[0][0])

	key = calculatePotentialKey(cipherText, likelyKeyLens[0][0])

	print('Trying key: %s' % key)

	message = vigenereDecryptWithKey(cipherText, key)

	return message

def vigenereDecryptWithKey(cipherText, key):
	message = []
	keyIndex = 0
	for c in cipherText:
		letterNum = Letters.find(c.upper())
		letterNum -= Letters.find(key[keyIndex])
		letterNum %= len(Letters)

		keyIndex += 1
		if keyIndex >= len(key):
			keyIndex = 0

		message.append(Letters[letterNum])

	return ''.join(message)

# Count collisions and return an ordered list of most likely lengths for the key
def calculateLikelyKeyLens(cipherText):
	coincidenceCounts = []
	shiftCipher = deque(cipherText)
	shiftCipher.rotate(1)

	for i in range(1, len(cipherText)):
		coincidenceCounts.append((i, countCoincidences(cipherText, i)))
		shiftCipher.rotate(1)

	return sortKeys(coincidenceCounts)

def countCoincidences(text, offset):
	coinCount = 0
	for i in range(0, len(text)-offset):
		if text[i] == text[i+offset]:
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