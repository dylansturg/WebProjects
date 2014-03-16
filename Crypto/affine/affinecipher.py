import sys
import numpy
from collections import deque
from ciphertext import CipherText
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
		key = (int(key[0:2]), int(key[2:]))

	if mode == 'decrypt':
		print(affineDecrypt(CipherText(text), key))

	if mode == 'encrypt':
		print(affineEncrypt(text, key))

def gcd(a, b):
	return numpy.core._internal._gcd(a, b)

def affineDecrypt(cipherText, encryptkey=None):
	decryptkey = ()
	if not encryptkey:
		raise ValueError('finding key is not yet supported')

	else:
		if gcd(encryptkey[0], len(Letters)) > 1:
			raise ValueError('invalid key: gcd > 1')

def extendedEuclidGcd(a, b):
	''' y = s, x = t '''
	xCoefs = [0, 1]
	yCoefs = [1, 0]
	remainders = [a, b]
	oldX, x, oldY, y, oldR, r = None, None, None, None, None, None
	i = 1
	while(remainders[i] != 0):
		q = remainders[i-1] // remainders[i]
		oldR, r = remainders[i], remainders[i-1] - q*remainders[i]
		oldY, y = yCoefs[i], yCoefs[i-1] - q * yCoefs[i]
		oldX, x = xCoefs[i], xCoefs[i-1] - q * xCoefs[i]

		xCoefs.append(x)
		yCoefs.append(y)
		remainders.append(r)
		i += 1

	print('Coeff (%s, %s)' % (xCoefs[i-1], yCoefs[i-1]))
	print('gcd %s' % remainders[i-1])

	return


def euclidQuotients(a, b):
	if a < b:
		a ^= b
		b ^= a
		a ^= b

	quotients = []
	remainders = []
	while(a > b):
		print('eculid %s, %s' % (a, b))
		q = a // b
		r = a % b
		a = b
		b = r
		quotients.append(q)
		remainders.append(r)
		if r == 0:
			break

	return quotients, remainders

def affineEncrypt(message, key):
	print('Encrypting with key (%s, %s)' % key)

	if gcd(key[0], len(Letters)) > 1:
		raise ValueError('invalid key: gcd > 1')

	shifter = affineShifterGen(key)

	cipherText = []
	for c in message:
		letterNum = Letters.find(c.upper())
		letterNum = shifter(letterNum) % len(Letters)
		cipherText.append(Letters[letterNum])

	return ''.join(cipherText).upper()

def affineShifterGen(key, decrypt = False):
	return lambda x: x*int(key[0]) + int(key[1]) if not decrypt else lambda x: int(key[0]) * (x - int(key[1]))

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

if __name__ == "__main__":
	main()