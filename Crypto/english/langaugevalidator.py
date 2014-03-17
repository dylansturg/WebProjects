import numpy
import english
from cryptotext import CryptoText

class LanguageValidator:

	@staticmethod
	def frequencyCorrelation(message):
		letterFrequencies = []
		try:
			letterFrequencies = message.countLetterFrequencies(english.AlphabetSize)
		except:
			message = CryptoText(message)
			letterFrequencies = message.countLetterFrequencies(english.AlphabetSize)

		return numpy.dot(english.LetterFrequencies, letterFrequencies)


