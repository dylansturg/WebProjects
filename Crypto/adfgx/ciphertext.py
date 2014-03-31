import re

''' CipherText
	String extension to provide extra operations for strings used as cipher text.
''' 
class CipherText(str):

	def generatePairs(self):
		for i in range(len(self)//2):
			yield self[2*i] + self[2*i+1]


