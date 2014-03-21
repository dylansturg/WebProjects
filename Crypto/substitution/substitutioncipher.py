import sys
from ciphertext import CipherText

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

	if '-info' in sys.argv:
		mode = "printstats"

	if '-d' in sys.argv:
		mode = 'decrypt'

	if '-k' in sys.argv:
		if len(sys.argv) < sys.argv.index('-k') + 1:
			print('add key after key flag')
			return
		key = sys.argv[sys.argv.index('-k')+1].upper()

	if mode == 'decrypt':
		print(substitutionDecrypt(CipherText(text), key))

	if mode == 'encrypt':
		print(substitutionEncrypt(text, key))

	if mode == "printstats":
		outfile = open("statsfile.txt", "w")
		prettyPrintFrequencies(CipherText(text), outfile)
		outfile.close()


def substitutionEncrypt(message, subkey):
	return message


def substitutionDecrypt(cipherText, subkey = None):
	return cipherText


def prettyPrintFrequencies(cipherText, outstream = None):
	print("\nSingles: ", file=outstream)
	singleLetters = cipherText.countLetterFrequencies()
	printFrequencies(singleLetters, outstream)

	print("\nDigraphs: ", file=outstream)

	digraphs = cipherText.countDigraphs()
	printFrequencies(digraphs, outstream)

	print("\nReversed Digraphs: ", file=outstream)
	reversedDigraphs = cipherText.findReversedDigraphs()
	for f in reversedDigraphs:
		print(str(f[0]) + " " + str(f[1]) + ", " + str(f[2]) + " " + str(f[3]) + " | ", file=outstream, end="")

	print("", file=outstream, flush=True)


	print("\nDouble Letters: ", file=outstream)

	doubles = cipherText.countDoubleLetters()
	printFrequencies(doubles, outstream)

	print("\nTrigraphs: ", file=outstream)

	trigraphs = cipherText.countTrigraphs()
	printFrequencies(trigraphs, outstream)

def printFrequencies(frequencies, outstream):
	for f in frequencies:
		print(str(f[0]) + " " + str(f[1]) + " | ", file=outstream, end="")

	print("", file=outstream, flush=True)

def parseFrequencies(filename):
	f = open(filename)
	data = f.read()
	data = remove(data, ["\n", "|", "-", "%"])

	freqs = data.split(" ")
	freqs = [i for i in freqs if i != '']

	frequencies = []
	for i in range(0, len(freqs)//3):
		frequencies.append((freqs[3*i], freqs[3*i+1], freqs[3*i+2]))

	frequencies = map(lambda x: (x[0], int(x[1]), float(x[2])/100), frequencies)	

	return sorted(frequencies, key=lambda x: x[1], reverse=True)

def remove(string, removals):
	result = string
	for r in removals:
		result = result.replace(r, " ")
	return result


if __name__ == "__main__":
	main()		