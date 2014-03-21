import re

''' CipherText
	String extension to provide extra operations for strings used as cipher text.
''' 
class CipherText(str):

	def countLetterFrequencies(self):
		frequencies = {}

		letterCount = len(self)
		for letter in self.upper():
			incrementHistogramDict(frequencies, letter)

		frequencies = calculateHistogramPercentages(frequencies, letterCount)
		return histogramToSortedList(frequencies)

	def countDigraphs(self):
		frequencies = {}

		diCount = 0
		for i in range(0, len(self)-1):
			digraph = self[i] + self[i+1]
			incrementHistogramDict(frequencies, digraph)
			diCount += 1

		frequencies = calculateHistogramPercentages(frequencies, diCount)

		return histogramToSortedList(frequencies)

	def countTrigraphs(self):
		frequencies = {}

		triCount = 0
		for i in range(0, len(self)-2):
			trigraph = self[i] + self[i+1] + self[i+2]
			incrementHistogramDict(frequencies, trigraph)
			triCount += 1

		frequencies = calculateHistogramPercentages(frequencies, triCount)
		return histogramToSortedList(frequencies)

	def countDoubleLetters(self):
		frequencies = {}

		doubleCount = 0
		for i in range(0, len(self)-1):
			if self[i] == self[i+1]:
				incrementHistogramDict(frequencies, self[i]*2)
				doubleCount += 1

		frequencies = calculateHistogramPercentages(frequencies, doubleCount)
		return histogramToSortedList(frequencies)

	def findReversedDigraphs(self):
		digraphs = self.countDigraphs()

		histogram = {}
		for digraph in digraphs:
			if digraph[0] not in histogram and digraph[0][::-1] not in histogram:
				histogram[digraph[0]] = 0
			else:
				if digraph[0] in histogram:
					histogram[digraph[0]] += 1
				elif digraph[0][::-1] in histogram:
					histogram[digraph[0][::-1]] += 1
				else:
					pass
		return histogram
		histogram = sorted(histogram, key=lambda x: x[1], reverse=True)
		return histogram
		duplicates = [x for x in histogram if x[1] > 0]
		return duplicates

	def applySubstitutionKey(self, subkey):
		result = str(self)
		for k in subkey:
			result = result.replace(k.upper(), subkey[k].lower())
		return CipherText(result)

def reverseEqual(s1, s2):
	return s1 == s2 or s1[::-1] == s2

def incrementHistogramDict(histogram, element):
	if element not in histogram:
		histogram[element] = 0
	histogram[element] += 1

def calculateHistogramPercentages(histogram, totalCount):
	for key in histogram:
		histogram[key] = (histogram[key], histogram[key]/totalCount)
	return histogram

def histogramToSortedList(histogram):
	ls = []
	for key in histogram:
		ls.append((key, histogram[key][0], histogram[key][1]))

	return sorted(ls, key=lambda x: x[1], reverse=True)

