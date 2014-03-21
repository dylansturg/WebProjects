import sys

def main():
	filename = None

	if len(sys.argv) < 1:
		print('Please include some arguments.')
		return

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

	if '-fo' in sys.argv:
		if len(sys.argv) <= sys.argv.index('-fo') + 1:
			print('Need an accompanying file name')
			return

		filename = sys.argv[sys.argv.index('-fo')+1]

	f = None
	if filename:
		f = open(filename, "w")

	fixText(text, f)


def fixText(text, outstream=None):
	result = text
	for c in text:
		if not c.isalpha():
			result = result.replace(c, '')
	result = result.lower()
	print(result, file=outstream)
	return result

if __name__ == "__main__":
	main()		