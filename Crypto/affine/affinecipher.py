import sys
import numpy
from collections import deque
from ciphertext import CipherText
from operator import itemgetter

sys.path.append("..")
sys.path.append("../english")
from english import english
from english import languagevalidator


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

		return crackAffine(ciphertext, english.AlphabetSize)["message"]
			

	else:
		if gcd(encryptkey[0], len(Letters)) > 1:
			raise ValueError('invalid key: gcd > 1')

		alphaInv, keyInv = extendedEuclidGcd(len(Letters), encryptkey[0])

		shifter = affineShifterGen((keyInv, encryptkey[1]), decrypt=True)

		return shiftMessageWithShifter(ciphertext, shifter).lower()

def crackAffine(ciphertext, alphabetSize):
	candidates = findAffineDecryptedCandidates(ciphertext, alphabetSize)

	for i in range(0, len(candidates), 5):
		for j in range(0, 5):
			print("Candidate %s: (Decrypt) Key %sx+%s: Correlation: %s" % (i+j, candidates[i+j]['key'][0], candidates[i+j]['key'][1], candidates[i+j]['correlation']))
			print("Message: %s" % (candidates[i+j]['message']))

		resp = input("Continue? y/n: ")
		if resp == 'n':
			cand = input("which one?: ")
			return candidates[int(cand)]


def findAffineDecryptedCandidates(ciphertext, alphabetSize):
	candidates = []

	for key in generatePotentialKeys(alphabetSize):
		cand = {}
		shifter = affineShifterGen(key, decrypt=True)
		cand['key'] = key
		cand['message'] = shiftMessageWithShifter(ciphertext, shifter).lower()
		cand['correlation'] = languagevalidator.LanguageValidator.frequencyCorrelation(cand['message'])
		candidates.append(cand)

	return sorted(candidates, key=lambda x: x['correlation'], reverse=True)

def generatePotentialKeys(alphabetSize):
	for multiplier in generateAllRelativelyPrimes(alphabetSize):
		for adder in range(0, alphabetSize):
			yield (multiplier, adder)

def generateAllRelativelyPrimes(upperBoundary):
	for i in range(1, upperBoundary):
		if gcd(i, upperBoundary) == 1:
			yield i

def extendedEuclidGcd(a, b):
	''' y = s, x = t '''
	bCoefs = [0, 1]
	aCoefs = [1, 0]
	remainders = [a, b]
	oldX, x, oldY, y, oldR, r = None, None, None, None, None, None
	i = 1
	while(remainders[i] != 0):
		q = remainders[i-1] // remainders[i]
		oldR, r = remainders[i], remainders[i-1] - q*remainders[i]
		oldY, y = aCoefs[i], aCoefs[i-1] - q * aCoefs[i]
		oldX, x = bCoefs[i], bCoefs[i-1] - q * bCoefs[i]

		bCoefs.append(x)
		aCoefs.append(y)
		remainders.append(r)
		i += 1

	return aCoefs[i-1], bCoefs[i-1]

def affineEncrypt(message, key):
	if gcd(key[0], len(Letters)) > 1:
		raise ValueError('invalid key: gcd > 1')

	shifter = affineShifterGen(key)

	return shiftMessageWithShifter(message, shifter).upper()

'''
	key of the form: (multiplier, adder)
'''
def affineShifterGen(key, decrypt = False):
	if not decrypt:
		return lambda x: x*int(key[0]) + int(key[1])
	else:
		return lambda x: int(key[0]) * (x - int(key[1]))

def shiftMessageWithShifter(text, shifter):
	message = []
	for c in text:
		letterNum = Letters.find(c.upper())
		letterNum = shifter(letterNum) % len(Letters)
		message.append(Letters[letterNum])

	return ''.join(message)

if __name__ == "__main__":
	main()