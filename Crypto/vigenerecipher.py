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

	if '-f' in sys.argv:
		if len(sys.argv) <= sys.argv.index('-f') + 1:
			print('Need an accompanying file name')
			return

		textFile = open(sys.argv[sys.argv.index('-f')+1])
		text = textFile.read()
		textFile.close()

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
		print(vigenereDecrypt(CipherText(text), key))

	if mode == 'encrypt':
		print(vigenereEncrypt(text, key))

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
		likelyKeyLens = VigenereKeyLengthSolver(cipherText)
		keyLen = next(likelyKeyLens.generateKeyLengths())
		possibleSolutions = []

		print('Trying key length: %s' % keyLen)

		key = next(VigenereKeySolver(cipherText, likelyKeyLens.generateKeyLengths()).calculatePotentialKey())

		print('Trying key: %s' % key)

	print ('using key %s' % key)

	message = shiftMessageWithKey(cipherText, key, lambda x, y: x - y).lower()

	return message

if __name__ == "__main__":
	main()