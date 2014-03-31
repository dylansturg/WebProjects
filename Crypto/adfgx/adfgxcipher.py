import sys
from ciphertext import CipherText
from adfgxgrid import AdfgxGrid
from adfgxkey import AdfgxKey, alphabetizeLetters

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
		print(adfgxDecrypt(CipherText(text), key))

	if mode == 'encrypt':
		print(adfgxEncrypt(text, key))

def adfgxEncrypt(message, alphabet, keyword):
	grid = AdfgxGrid(alphabet)
	key = AdfgxKey(keyword)
	cipherText = grid.encodeMessage(message.replace(" ", ""))
	res = key.encryptMessage(cipherText)

	return res

def adfgxDecrypt(message, alphabet, keyword):
	res = ''
	grid = AdfgxGrid(alphabet)
	key = AdfgxKey(alphabetizeLetters(keyword))

	keyDecrypted = key.encryptMessage(message, key=keyword)

	res = grid.decodeMessage(keyDecrypted)

	return res


if __name__ == "__main__":
	main()		