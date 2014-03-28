import json

Letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'



class SubstitutionKey(dict):

	def __init__(self, keyText=None):
		try:
			key = eval(keyText)
		except:
			key = keyText
		if checkIfDictionaryLike(key):
			for k in key:
				self[k] = key[k]

		

	def addKey(self, cipherLetter, messageLetter):
		cipherLetter = cipherLetter.upper()
		messageLetter = messageLetter.lower()
		if len(cipherLetter) != len(messageLetter):
			raise Exception
		for i in range(0, len(cipherLetter)):
			if cipherLetter[i] not in self:
				self[cipherLetter[i]] = messageLetter[i]
			else:
				print("That letter is already in the key")

	def removeKey(self, cipherLetter):
		self.pop(cipherLetter, None)

	def reportMissingLetters(self):
		decodedLetters = []
		for k in self:
			decodedLetters.append(self[k])

		missingDecryptLetters = []
		for l in Letters.lower():
			if l not in decodedLetters:
				missingDecryptLetters.append(l)

		encodedLetters = []
		for k in self:
			encodedLetters.append(k)

		missingEncryptLetters = []
		for l in Letters.upper():
			if l not in encodedLetters:
				missingEncryptLetters.append(l)

		return (missingDecryptLetters, missingEncryptLetters)

	def write(self, outstream):
		json.dump(self, outstream)

	def read(self, instream):
		data = json.load(instream)

		for k in data:
			self[k] = data[k]


def checkIfDictionaryLike(test):
	try:
		test['']
		return True
	except KeyError:
		return True
	except:
		return False