class SubstitutionKey:
	keyMap = dict()

	def __init__(self, keyText):
		key = eval(keyText)
		if checkIfDictionaryLike(key):
			keyMap = key

		for k in key:
			keyMap[k[0]] = k[1]

	


def checkIfDictionaryLike(test):
	try:
		test['']
		return True
	except KeyError:
		return True
	except:
		return False