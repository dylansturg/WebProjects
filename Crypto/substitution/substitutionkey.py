class SubstitutionKey(dict):

	def __init__(self, keyText=None):

		try:
			key = eval(keyText)
		except:
			return
		if checkIfDictionaryLike(key):
			for k in key:
				self[k] = key[k]

		for k in key:
			self[k[0]] = k[1]

	def addKey(self, cipherLetter, messageLetter):
		if cipherLetter not in self:
			self[cipherLetter] = messageLetter
		else:
			print("That letter is already in the key")

	def removeKey(self, cipherLetter):
		self.pop(cipherLetter, None)


def checkIfDictionaryLike(test):
	try:
		test['']
		return True
	except KeyError:
		return True
	except:
		return False