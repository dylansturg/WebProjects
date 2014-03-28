import sys
from ciphertext import CipherText
from playfairgrid import PlayfairGrid

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
		print(playfairDecrypt(CipherText(text), key))

	if mode == 'encrypt':
		print(playfairEncrypt(text, key))

def playfairEncrypt(message, keyword):
	res = ''
	grid = PlayfairGrid(keyword)
	for digraph in CipherText(message).generatePlayfairDigraphs():
		res += grid.encodeDigraph(digraph)
	return res

def playfairDecrypt(cipher, keyword):
	res = ''
	grid = PlayfairGrid(keyword)
	for digraph in CipherText(cipher).generatePlayfairDigraphs():
		res += grid.decodeDigraph(digraph)

	return res.lower()



if __name__ == "__main__":
	main()		