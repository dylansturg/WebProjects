''' CipherText
	String extension to provide extra operations for strings used as cipher text.
''' 
class CipherText(str):

	def countLetterFrequencies(self, AlphabetSize):
		frequencies = []
		freqLen = 0

		for i in range(0, AlphabetSize):
			frequencies.append(0)

		freqLen = len(frequencies)

		letterCount = len(self)
		for letter in self.upper():
			index = ord(letter) - ord('A')
			if(freqLen <= index):
				for i in range(freqLen, index+1):
					frequencies.append(0)
				freqLen = index+1

			frequencies[index] += 1

		return list(map(lambda x: x/letterCount, frequencies))