#
# TODO: Migrate this to jk_utils and jk_valueformatting.
#



import typing

import jk_console






#
# Formats a value provided in bits per second.
#
# @param	float value			A value (measured in bits per second).
# @returns	float value			The scaled value.
# @returns	str unit			The unit of the value, e.g. "Gbit/s".
#
def formatBitsPerSecond(value:float, floatPrecision:bool = False) -> tuple:
	m = 1000
	if floatPrecision:
		if value >= m:
			if value >= m*m:
				if value >= m*m*m:
					value = int(value / (m*m*m) * 10 + 0.5) / 10
					unit = "Gbit/s"
				else:
					value = int(value / (m*m) * 10 + 0.5) / 10
					unit = "Mbit/s"
			else:
				value = value / m
				unit = "Kbit/s"
		else:
			unit = "bit/s"
	else:
		if value >= m:
			if value >= m*m:
				if value >= m*m*m:
					value = value // (m*m*m)
					unit = "Gbit/s"
				else:
					value = value // (m*m)
					unit = "Mbit/s"
			else:
				value = value // m
				unit = "Kbit/s"
		else:
			unit = "bit/s"
	return value, unit
#



#
# Same as <c>formatBitsPerSecond()</c> but does not return a tuple but a string.
#
def formatBitsPerSecondS(value:float, floatPrecision:bool = False) -> str:
	value, unit = formatBitsPerSecond(value, floatPrecision)
	return str(value) + " " + unit
#



#
# Formats a value provided in bytes.
#
# @param	float value			A value (measured in bytes).
# @returns	float value			The scaled value.
# @returns	str unit			The unit of the value, e.g. "Gbyte".
#
def formatBytes(value:typing.Union[float,int], floatPrecision:bool = True, magOverride:str = None) -> typing.Tuple[float,str]:
	m = 1024
	value = float(value)

	if magOverride:
		_magOverr = magOverride.lower()

		if floatPrecision:
			if _magOverr in ( "tbyte", "tb", ):
				value = int(value / (m*m*m*m) * 10 + 0.5) / 10
				unit = "TByte"
			elif _magOverr in ( "gbyte", "gb", ):
				value = int(value / (m*m*m) * 10 + 0.5) / 10
				unit = "GByte"
			elif _magOverr in ( "mbyte", "mb", ):
				value = int(value / (m*m) * 10 + 0.5) / 10
				unit = "MByte"
			elif _magOverr in ( "kbyte", "kb", ):
				value = int(value / m * 10 + 0.5) / 10
				unit = "KByte"
			elif _magOverr in ( "byte", "b", ):
				unit = "Byte"
			else:
				raise Exception("Unsupported magnitude specified: " + repr(magOverride))

		else:
			if _magOverr in ( "tbyte", "tb", ):
				value = int(value) // m*m*m*m
				unit = "TByte"
			elif _magOverr in ( "gbyte", "gb", ):
				value = int(value) // m*m*m
				unit = "GByte"
			elif _magOverr in ( "mbyte", "mb", ):
				value = int(value) // m*m
				unit = "MByte"
			elif _magOverr in ( "kbyte", "kb", ):
				value = int(value) // m
				unit = "KByte"
			elif _magOverr in ( "byte", "b", ):
				value = int(value)
				unit = "Byte"
			else:
				raise Exception("Unsupported magnitude specified: " + repr(magOverride))

	else:

		if floatPrecision:
			if value >= m:
				if value >= m*m:
					if value >= m*m*m:
						if value >= m*m*m*m:
							value = int(value / (m*m*m*m) * 10 + 0.5) / 10
							unit = "TByte"
						else:
							value = int(value / (m*m*m) * 10 + 0.5) / 10
							unit = "GByte"
					else:
						value = int(value / (m*m) * 10 + 0.5) / 10
						unit = "MByte"
				else:
					value = int(value / m * 10 + 0.5) / 10
					unit = "KByte"
			else:
				unit = "Byte"

		else:
			if value >= m:
				if value >= m*m:
					if value >= m*m*m:
						if value >= m*m*m*m:
							value = int(value) // m*m*m*m
							unit = "TByte"
						else:
							value = int(value) // m*m*m
							unit = "GByte"
					else:
						value = int(value) // m*m
						unit = "MByte"
				else:
					value = int(value) // m
					unit = "KByte"
			else:
				value = int(value)
				unit = "Byte"

	return value, unit
#

#
# Get the magnitude of the specified value or values.
#
def getBytesMagnitude(*values:typing.Iterable[typing.Union[float,int]]) -> str:
	m = 1024

	if len(values) == 0:
		return "Byte"

	value = max(*values)

	if value >= m:
		if value >= m*m:
			if value >= m*m*m:
				if value >= m*m*m*m:
					return "TByte"
				else:
					return "GByte"
			else:
				return "MByte"
		else:
			return "KByte"
	else:
		return "Byte"
#

def formatBytesS(value:float, floatPrecision:bool = True, magOverride:str = None) -> str:
	value, unit = formatBytes(value, floatPrecision, magOverride)
	return str(value) + " " + unit
#



#
# Formats a value provided in Herz.
#
# @param	float value			A value (measured in Herz).
# @returns	float value			The scaled value.
# @returns	str unit			The unit of the value, e.g. "GHz".
#
def formatFrequency(value:float, floatPrecision:bool = True) -> tuple:
	if floatPrecision:
		if value >= 1000:
			if value >= 1000000:
				if value >= 1000000000:
					value = (value / 1000000000 * 10 + 0.5) / 10
					unit = "GHz"
				else:
					value = (value / 1000000 * 10 + 0.5) / 10
					unit = "MHz"
			else:
				value = (value / 1000 * 10 + 0.5) / 10
				unit = "KHz"
		else:
			unit = "Hz"
	else:
		if value >= 1000:
			if value >= 1000000:
				if value >= 1000000000:
					value = value // 1000000000
					unit = "GHz"
				else:
					value = value // 1000000
					unit = "MHz"
			else:
				value = value // 1000
				unit = "KHz"
		else:
			unit = "Hz"
	return value, unit
#

def formatFrequencyS(value:float, floatPrecision:bool = True) -> str:
	value, unit = formatFrequency(value, floatPrecision)
	return str(value) + " " + unit
#



#
# Formats a value provided in Herz.
#
# @param	float value1			A value (measured in Herz).
# @param	float value2			A value (measured in Herz).
# @returns	float value1			The scaled value 1.
# @returns	float value2			The scaled value.2.
# @returns	str unit				The unit of the value, e.g. "GHz".
#
def formatFrequencyRange(value1:float, value2:float, floatPrecision:bool = True) -> tuple:
	if floatPrecision:
		value = max(value1, value2)
		if value >= 1000:
			if value >= 1000000:
				if value >= 1000000000:
					value1 = (value1 / 1000000000 * 10 + 0.5) / 10
					value2 = (value2 / 1000000000 * 10 + 0.5) / 10
					unit = "GHz"
				else:
					value1 = (value1 / 1000000 * 10 + 0.5) / 10
					value2 = (value2 / 1000000 * 10 + 0.5) / 10
					unit = "MHz"
			else:
				value1 = (value1 / 1000 * 10 + 0.5) / 10
				value2 = (value2 / 1000 * 10 + 0.5) / 10
				unit = "KHz"
		else:
			unit = "Hz"
	else:
		value = min(value1, value2)
		if value >= 1000:
			if value >= 1000000:
				if value >= 1000000000:
					value1 = value1 // 1000000000
					value2 = value2 // 1000000000
					unit = "GHz"
				else:
					value1 = value1 // 1000000
					value2 = value2 // 1000000
					unit = "MHz"
			else:
				value1 = value1 // 1000
				value2 = value2 // 1000
				unit = "KHz"
		else:
			value1 = int(value1)
			value2 = int(value2)
			unit = "Hz"
	return value1, value2, unit
#

def formatFrequencyRangeS(value1:float, value2:float, floatPrecision:bool = True) -> str:
	value1, value2, unit = formatFrequencyRange(value1, value2, floatPrecision)
	return str(value1) + "-" + str(value2) + " " + unit
#



def formatPercent(value:float, total:float) -> str:
	return str(int(value / total * 1000) / 10) + "%"
#



#
# @param	float fromColorR		Red spectrum part ranging from 0 to 1
# @param	float fromColorG		Green spectrum part ranging from 0 to 1
# @param	float fromColorB		Blue spectrum part ranging from 0 to 1
# @param	float toColorR			Red spectrum part ranging from 0 to 1
# @param	float toColorG			Green spectrum part ranging from 0 to 1
# @param	float toColorB			Blue spectrum part ranging from 0 to 1
# @param	int length				The number of color values to create
# @return	list					An array of strings with color escape codes
#
def _createColorSpectrum(fromColorR:float, fromColorG:float, fromColorB:float, toColorR:float, toColorG:float, toColorB:float, length:int):
	ret = []
	for i in range(0, length):
		v = i / (length -1)
		vv = 1 - v
		r = fromColorR * vv + toColorR * v
		g = fromColorG * vv + toColorG * v
		b = fromColorB * vv + toColorB * v
		ret.append(jk_console.Console.ForeGround.rgb1(r, g, b))
	return ret
#

#
# Build a graph showing fill grade in percentage
#
# @param	float value			The current value. This can be an arbitrary value greater than zero and smaller than <c>total</c>.
# @param	float total			The maximum value. This can be an arbitrary value greater than <c>value</c>.
# @param	int length			The length of the bar to produce.
#
def formatPercentGraphC(value:float, total:float, length:int = 40) -> str:
	n = int(value / total * length)
	s = "#" * n

	colorSpectrum1 = _createColorSpectrum(0.7, 0.7, 0.7, 0.7, 0.7, 0, int(length * 0.1))
	colorSpectrum2 = _createColorSpectrum(0.7, 0.7, 0,   1,   0.5, 0, int(length * 0.1))
	colorSpectrum3 = _createColorSpectrum(1,   0.5, 0,   1,   0,   0, int(length * 0.1))
	colorSpectrum4 = _createColorSpectrum(1,   0,   0,   1,   0,   0, int(length * 0.05))
	colorSpectrum = colorSpectrum1 + colorSpectrum2 + colorSpectrum3 + colorSpectrum4
	posStart = length - len(colorSpectrum)

	bColorAdded = False
	for pos in range(len(s) - 1, -1, -1):
		i = pos - posStart
		if i < 0:
			break
		s = s[:pos] + colorSpectrum[i] + s[pos:]
		bColorAdded = True

	if bColorAdded:
		s += jk_console.Console.RESET

	s += ":" * (length - n)
	return s
#

def formatTemperatureGraphC2(value:float, maximum:float = 100, length:int = 40) -> typing.Tuple[str,str]:
	assert isinstance(value, (int, float))
	assert isinstance(maximum, (int, float))
	assert isinstance(length, int)

	# ----

	orgValue = value
	if value < 0:
		value = 0
	if value > maximum:
		value = maximum

	n = int(value / maximum * length)
	s = "#" * n

	colorSpectrum1 = _createColorSpectrum(0.7, 0.7, 0.7, 0.7, 0.7, 0, int(length * 0.23))
	colorSpectrum2 = _createColorSpectrum(0.7, 0.7, 0,   1,   0.5, 0, int(length * 0.23))
	colorSpectrum3 = _createColorSpectrum(1,   0.5, 0,   1,   0,   0, int(length * 0.23))
	colorSpectrum = colorSpectrum1 + colorSpectrum2 + colorSpectrum3
	posStart = length - len(colorSpectrum)

	firstColor = ""
	bColorAdded = False
	for pos in range(len(s) - 1, -1, -1):
		i = pos - posStart
		if i < 0:
			break
		s = s[:pos] + colorSpectrum[i] + s[pos:]
		if not bColorAdded:
			firstColor = colorSpectrum[i]
			bColorAdded = True

	if bColorAdded:
		s += jk_console.Console.RESET

	s += ":" * (length - n)

	s2 = str(int(orgValue + 0.5)) + "°C"

	return (
		s,
		firstColor + s2 + jk_console.Console.RESET
	)
#

def formatTemperatureGraphC(value:float, maximum:float = 100, length:int = 40) -> str:
	x = formatTemperatureGraphC2(value, maximum, length)
	return x[1] + " " + x[3]
#

def convertSecondsToHumanReadableDuration(seconds:float) -> typing.Tuple[int,int,int,int,float]:
	milliseconds = (seconds - int(seconds)) * 1000
	seconds = int(seconds)

	minutes = seconds // 60
	seconds = seconds % 60

	hours = minutes // 60
	minutes = minutes % 60

	days = hours // 24
	hours = hours % 24

	return days, hours, minutes, seconds, milliseconds
#












