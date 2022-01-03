

import re
import os

import jk_cmdoutputparsinghelper
from jk_cachefunccalls import cacheCalls
#import jk_json

from .parsing_utils import *
from .invoke_utils import run





class DMIDecodeConstants:

	BIOS = 0
	SYSTEM = 1
	BASE_BOARD = 2
	CHASSIS = 3
	PROCESSOR = 4
	MEMORY_CONTROLLER = 5
	MEMORY_MODULE = 6
	CPU_CACHE = 7
	PORT_CONNECTOR = 8
	SYSTEM_SLOTS = 9
	ON_BOARD_DEVICES = 10
	OEM_STRINGS = 11
	SYSTEM_CONFIGURATION_OPTIONS = 12
	BIOS_LANGUAGE = 13
	GROUP_ASSOCIATIONS = 14
	SYSTEM_EVENT_LOG = 15
	PHYSICAL_MEMORY_ARRAY = 16
	MEMORY_DEVICE = 17
	MEMORY_ERROR_32_BIT = 18
	MEMORY_ARRAY_MAPPED_ADDRESS = 19
	MEMORY_DEVICE_MAPPED_ADDRESS = 20
	BUILT_IN_POINTING_DEVICE = 21
	PORTABLE_BATTERY = 22
	SYSTEM_RESET = 23
	HARDWARE_SECURITY = 24
	SYSTEM_POWER_CONTROLS = 25
	VOLTAGE_PROBE = 26
	COOLING_DEVICE = 27
	TEMPERATURE_PROBE = 28
	ELECTRICAL_CURRENT_PROBE = 29
	OUT_OF_BAND_REMOTE_ACCESS = 30
	BOOT_INTEGRITY_SERVICES = 31
	SYSTEM_BOOT = 32
	MEMORY_ERROR_64_BIT = 33
	MANAGEMENT_DEVICE = 34
	MANAGEMENT_DEVICE_COMPONENT = 35
	MANAGEMENT_DEVICE_THRESHOLD_DATA = 36
	MEMORY_CHANNEL = 37
	IPMI_DEVICE = 38
	POWER_SUPPLY = 39
	ADDITIONAL_INFORMATION = 40
	ONBOARD_DEVICE = 41

#






def _parse_block(lineList:jk_cmdoutputparsinghelper.LineList) -> dict:
	assert isinstance(lineList, jk_cmdoutputparsinghelper.LineList)

	# lineList.dump()

	assert not lineList[0].startswith("\t")
	assert not lineList[1].startswith("\t")
	if len(lineList) == 2:
		# empty
		return {}
	assert lineList[2].startswith("\t")

	m = re.match("^Handle 0x([0-9A-Fa-f]+), DMI type ([0-9]+), .*", lineList[0])
	if m is None:
		raise Exception("Parse error: " + repr(lineList[0]))

	retData = {}
	ret = {
		"handle": m.group(1),
		"blockType": lineList[1],
		"data": retData,
	}

	# extract data

	lineList = lineList.extractFromTo(2)
	if not lineList.hasCommonPrefix("\t"):
		raise Exception("Parse error: \\t is not a common prefix")
	lineList.removeCommonPrefix("\t")

	# parse data

	_lastKey = None
	_lastValue = None
	_currentList = None
	for line in lineList:
		if line.startswith("\t"):
			# indented line
			if _currentList is not None:
				_currentList.append(line.strip())
			else:
				if _lastKey == "Items":
					# "Items" seems to be a marker for a list, though there is a value
					_currentList = [ line.strip() ]
					retData["Items"] = _currentList
				else:
					# ignore lines that belong to a list but where the kast key had a value
					#print("WARN: " + repr(line))
					#print("\t_lastKey: " + repr(_lastKey))
					#print("\t_lastValue: " + repr(_lastValue))
					pass
			_lastValue = None
		else:
			# regular data line
			pos = line.find(":")
			if pos < 0:
				raise Exception("Parse error: " + repr(line))
			_key = line[:pos]
			_value = line[pos+1:].strip()
			if _value:
				# we have a real value -> we typically don't have a list
				#print("#>>value#", repr(_key), repr(_value), len(_value))
				retData[_key] = _value
				_currentList = None
			else:
				# value is empty -> we have a list
				#print("#>>list#", repr(_key))
				_currentList = []
				retData[_key] = _currentList
				_value = None
			_lastKey = _key
			_lastValue = _value

	# ----

	#jk_json.prettyPrint(ret)
	return ret
#


#
#
#
def parse_dmi_decode(stdout:str, stderr:str, exitcode:int) -> typing.Union[list,None]:
	lineList = jk_cmdoutputparsinghelper.LineList(stdout.split("\n"))
	#lineList.dump()

	lineList.rightTrimAllLines()

	assert lineList
	assert lineList[0].startswith("# dmidecode ")
	if lineList[1].find("sorry") >= 0:
		# no dmidecode available
		return None

	# find empty section
	pos = lineList.findExact("")
	if pos < 0:
		raise Exception("Parse error!")
	lineList = lineList.extractFromTo(pos + 1)
	lineList.removeLeadingEmptyLines()
	lineList.removeTrailingEmptyLines()

	if len(lineList) == 0:
		# empty
		return []

	# ----------------------------------------------------------------

	ret = []
	blocks = lineList.splitAtEmptyLines()
	for block in blocks:
		ret.append(_parse_block(block))
 
	return ret
# 






def get_dmi_decode(c = None, typeNumberOrNumbers:typing.Union[int,typing.List[int],typing.Tuple[int]] = None) -> typing.Union[list,None]:
	if isinstance(typeNumberOrNumbers, (list,tuple)):
		sTypeNos = ",".join([ str(x) for x in typeNumberOrNumbers ])
	else:
		assert isinstance(typeNumberOrNumbers, int)
		sTypeNos = str(typeNumberOrNumbers)

	stdout, stderr, exitcode = run(c, "sudo /usr/sbin/dmidecode --type " + sTypeNos)
	return parse_dmi_decode(stdout, stderr, exitcode)
#










