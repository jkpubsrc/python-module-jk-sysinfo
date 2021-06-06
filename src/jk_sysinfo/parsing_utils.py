#
# This file contains various functions that assist in parsing.
# As a lot of tools require similar routines all these routines are factored out into this python file.
#


import typing



# copied to jk_cmdoutputparsinghelper
def parseKByteWithUnit(s:str):
	assert isinstance(s, str)

	if s.endswith(" KB"):
		return int(s[:-3])
	else:
		raise Exception("Can't be parsed: " + repr(s))
#



# copied to jk_cmdoutputparsinghelper
def splitAtEmptyLines(lines):
	ret = []
	buffer = []
	for line in lines:
		if line:
			buffer.append(line)
		else:
			if buffer:
				ret.append(buffer)
				buffer = []
	if buffer:
		ret.append(buffer)
		buffer = []
	return ret
#



# copied to jk_cmdoutputparsinghelper
def getPositionsOfWords(line:str) -> list:
	ret = []
	bLastWasSpace = True
	for i, c in enumerate(line):
		if c.isspace():
			bLastWasSpace = True
		else:
			if bLastWasSpace:
				ret.append(i)
			bLastWasSpace = False
	return ret
#



# copied to jk_cmdoutputparsinghelper
def isVerticalSpaceColumn(lines:str, pos:int) -> bool:
	for i in range(0, len(lines)):
		line = lines[i]
		if pos < len(line):
			if not line[pos].isspace():
				#print("@ " + str(pos) + " with " + repr(line[pos]) + " of " + repr(line))
				return False
	#print("@ " + str(pos) + " is space")
	return True
#



def countDownCounter(i:int, maxValue:int = 0):
	if i < maxValue:
		return
	yield i
	while True:
		i -= 1
		if i < maxValue:
			return
		yield i
#



def lineSplitAt(line:str, splitPositions:list, bTrim:bool = True):
	ret = []
	lastPos = 0
	for p in splitPositions:
		s = line[lastPos:p]
		if bTrim:
			s = s.strip()
		ret.append(s)
		lastPos = p
	s = line[lastPos:]
	if bTrim:
		s = s.strip()
	ret.append(s)
	return ret
#

# copied to jk_cmdoutputparsinghelper
def removeAllCommonLeadingSpaces(lines:list) -> list:
	# count leading spaces
	counts = []
	for line in lines:
		for n, c in enumerate(line):
			if not c.isspace():
				if n == 0:
					# premature end: this is a line beginning with a regular character
					return lines
				counts.append(n)
				break
	minPos = min(counts)
	return [ s[minPos:] for s in lines ]
#

def groupLinesByLeadingSpace(lines:list) -> dict:
	ret = {}
	lastLineData = None
	minNumOfSpaces = 99999999999999999999
	for i, line in enumerate(lines):
		if line[0].isspace():
			numberOfSpaces = len(line) - len(line.lstrip())
			if numberOfSpaces < minNumOfSpaces:
				minNumOfSpaces = numberOfSpaces
			lastLineData.append(line)
		else:
			if minNumOfSpaces != 99999999999999999999:
				for i, s in enumerate(lastLineData):
					lastLineData[i] = s[minNumOfSpaces:]
			lastLineData = []
			ret[line] = lastLineData
			minNumOfSpaces = 99999999999999999999

	if minNumOfSpaces != 99999999999999999999:
		for i, s in enumerate(lastLineData):
			lastLineData[i] = s[minNumOfSpaces:]

	return ret
#


# copied to jk_cmdoutputparsinghelper
class ParseAtFirstDelimiter(object):

	def __init__(self, delimiter:str = ":", valueCanBeWrappedInDoubleQuotes:bool = False, keysReplaceSpacesWithUnderscores:bool = False):
		self.delimiter = delimiter
		self.keysReplaceSpacesWithUnderscores = keysReplaceSpacesWithUnderscores
		self.valueCanBeWrappedInDoubleQuotes = valueCanBeWrappedInDoubleQuotes
	#

	def parseLines(self, lines):
		assert isinstance(lines, (tuple, list))

		ret = {}
		for line in lines:
			k, v = self.parseLine(line)
			if k:
				ret[k] = v
		#
		return ret
	#

	def parseLine(self, line:str):
		assert isinstance(line, str)

		pos = line.find(self.delimiter)
		if pos > 0:
			k = line[:pos].strip()
			v = line[pos+1:].strip()
			if self.valueCanBeWrappedInDoubleQuotes:
				if v.startswith("\"") and v.endswith("\""):
					v = v[1:-1]
					v = v.replace("\\\"", "\"")
			if self.keysReplaceSpacesWithUnderscores:
				k = k.replace(" ", "_")
			return k, v
		else:
			return None, None
	#

#




def simplifyValueList(valueList:typing.Union[None,list,tuple]) -> typing.Union[None,list]:
	if valueList is None:
		return None
	assert isinstance(valueList, (tuple, list))

	# group values by unit
	temp = {}
	for item in valueList:
		assert isinstance(item, dict)
		value = item["value"]
		unit = item["unit"]
		temp2 = temp.get(unit)
		if temp2 is None:
			temp2 = []
			temp[unit] = temp2
		temp2.append(value)
	
	# unwind temp

	ret = []
	for unit, valueList in temp.items():
		if len(valueList) > 0:
			ret.append({
				"unit": unit,
				"values": valueList
			})
		else:
			ret.append({
				"unit": unit,
				"value": valueList[0]
			})

	if len(ret) == 0:
		return None
	if len(ret) == 1:
		return ret[0]
	return ret
#



def joinDictsByKey(*args):
	ret = {}
	for dictionary in args:
		assert isinstance(dictionary, dict)
		for key, d in dictionary.items():
			assert isinstance(d, dict)
			for key2, value in d.items():
				if key not in ret:
					ret[key] = {}
				ret[key][key2] = value
	return ret
#









