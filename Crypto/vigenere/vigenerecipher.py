import sys
import numpy
from collections import deque
from ciphertext import CipherText
from vigenerekey import VigenereKeyLengthSolver, VigenereKeySolver
from operator import itemgetter


AsciiOffset = 65
Letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main():
	if len(sys.argv) < 1:
		print('Please include some arguments.')
		return

	mode = 'encrypt'
	text = ''
	key = None
	outfile = None

	if '-f' in sys.argv:
		if len(sys.argv) <= sys.argv.index('-f') + 1:
			print('Need an accompanying file name')
			return

		textFile = open(sys.argv[sys.argv.index('-f')+1])
		text = textFile.read()
		textFile.close()

	if '-fo' in sys.argv:
		if len(sys.argv) <= sys.argv.index('-fo') + 1:
			print('Need an accompanying file name')
			return

		outfile = open(sys.argv[sys.argv.index('-fo')+1], "w")

	if '-t' in sys.argv:
		if len(sys.argv) <= sys.argv.index('-t') + 1:
			print('Need ciper text')
			return

		text = sys.argv[sys.argv.index('-t')+1]

	if '-d' in sys.argv:
		mode = 'decrypt'

	if '-k' in sys.argv:
		if len(sys.argv) < sys.argv.index('-k') + 1:
			print('add key after key flag')
			return
		key = sys.argv[sys.argv.index('-k')+1].upper()

	if mode == 'decrypt':
		print(vigenereDecrypt(CipherText(text), key), file=outfile)

	if mode == 'encrypt':
		print(vigenereEncrypt(text, key), file=outfile)

def vigenereEncrypt(message, key):
	if not key:
		raise ValueError('Missing encryption key')

	return shiftMessageWithKey(message, key, lambda x, y: x + y)

def shiftMessageWithKey(text, key, shifter):
	message = []
	keyIndex = 0
	key = key.upper()
	for c in text:
		letterNum = Letters.find(c.upper())
		letterNum = shifter(letterNum, Letters.find(key[keyIndex]))
		letterNum %= len(Letters)

		keyIndex += 1
		if keyIndex >= len(key):
			keyIndex = 0

		message.append(Letters[letterNum])

	return ''.join(message)

def vigenereDecrypt(cipherText, key=None):

	if not key:
		return crackVigenereWithInput(cipherText)

	print ('using key %s' % key)

	message = shiftMessageWithKey(cipherText, key, lambda x, y: x - y).lower()

	return message

def crackVigenereWithInput(cipherText):
	keySolver = VigenereKeySolver(cipherText, VigenereKeyLengthSolver(cipherText).generateKeyLengths())
	keyGenerator = keySolver.calculatePotentialKeys()

	keyGuess = None

	while(True):

		if not keyGuess:
			try:
				keyGuess = next(keyGenerator)
			except StopIteration:
				keyGenerator = keySolver.calculatePotentialKeys()
				keyGuess = next(keyGenerator)

		print("Best key guess: %s" % keyGuess)
		print("Resulting message:")
		message = shiftMessageWithKey(cipherText, keyGuess, lambda x, y: x - y).lower()
		print(message)

		keyGuess = parseInput(keyGuess)
		if keyGuess == -1:
			return message


def parseInput(keyGuess):
	resp = input("Enter response: ").split(" ")

	if "stop" in resp:
		return -1

	if "try" in resp:
		keyGuess = resp[resp.index("try")+1].upper()

	if "replace" in resp:
		index = int(resp[resp.index("replace")+1])
		rep = resp[resp.index("replace")+2]
		keyGuess = list(keyGuess)
		keyGuess[index] = rep
		keyGuess = "".join(keyGuess).upper()

	if "go" in resp:
		keyGuess = None


	return keyGuess

if __name__ == "__main__":
	main()