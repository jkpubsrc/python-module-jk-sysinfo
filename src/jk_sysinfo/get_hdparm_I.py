

import datetime
from typing import NoReturn
import pytz
from dateutil import tz

from jk_cachefunccalls import cacheCalls
import jk_cmdoutputparsinghelper

from .parsing_utils import *
from .invoke_utils import run
from .get_date import *









_VALUE_PARSER_WITH_UNIT = jk_cmdoutputparsinghelper.ValueParser_ByteWithUnit()





class _LineGroup(object):

	def __init__(self, lineList:jk_cmdoutputparsinghelper.LineList) -> None:
		self.title = lineList[0]
		self.lines = lineList.extractFromTo(1)
		if self.lines:
			self.lines.removeCommonPrefix("\t")
	#

	def dump(self):
		print(self.title)
		self.lines.dump(prefix="\t")
	#

	def splitAt(self, lineText:str) -> tuple:
		#for i in range(0, len(self.lines)):
		#	print("-\t", repr(self.lines[i]), repr(lineText), self.lines[i] == lineText)

		n = self.lines.findExact(lineText)
		if n <= 0:
			return None, None

		return (
			self.lines.extractFromTo(0, n),
			self.lines.extractFromTo(n + 1),
		)
	#

#

class _GeneralBlock(object):

	"""
		ATA device, with non-removable media

		'Model Number:       xxxxxxxxxxxxxxxxxxxxxx',
		'Serial Number:      xxxxxxxxxxxx',
		'Firmware Revision:  xxxxxxx',
		'Transport:          Serial, ATA8-AST, SATA 1.0a, SATA II Extensions, SATA Rev 2.5, SATA Rev 2.6, SATA Rev 3.0',
	"""

	def __init__(self, lineGroup:_LineGroup) -> None:
		self.deviceType = lineGroup.title
		_map = lineGroup.lines.convertToMapAtDelimIfPossible(":")
		self.model = _map["Model Number"]
		self.serial = _map["Serial Number"]
		self.firmwareRevision = _map["Firmware Revision"]
		self.transport = _map["Transport"]
	#

	def toJSON(self) -> dict:
		return {
			"model": self.model,
			"serial": self.serial,
			"firmwareRevision": self.firmwareRevision,
			"transport": self.transport,
		}
	#

#

class _DriveConfigurationBlock(object):

	"""
		'Logical\t\tmax\tcurrent',
		'cylinders\t16383\t0',
		'heads\t\t16\t0',
		'sectors/track\t63\t0',
		'--',
		'LBA    user addressable sectors:   268435455',
		'LBA48  user addressable sectors:  1953525168',
		'Logical  Sector size:                   512 bytes',
		'Physical Sector size:                  4096 bytes',
		'Logical Sector-0 offset:                  0 bytes',
		'device size with M = 1024*1024:      953869 MBytes',
		'device size with M = 1000*1000:     1000204 MBytes (1000 GB)',
		'cache/buffer size  = unknown',
		'Form Factor: 2.5 inch',
		'Nominal Media Rotation Rate: Solid State Device',
	"""

	def __init__(self, lineGroup:_LineGroup) -> None:
		#lineGroup.dump()
		_partA, _partB = lineGroup.splitAt("--")

		if _partA is None:
			raise Exception("Parsing error!")

		# ----------------------------------------------------------------
		# parse part A

		assert len(_partA) == 4
		#_cyls = _partA[1].split("\t")
		#_heads = _partA[2].split("\t")
		#_sectors = _partA[3].split("\t")

		# ----------------------------------------------------------------
		# parse part B

		_map = _partB.convertToMapAtDelimIfPossible(":")

		self.maxLBA48Sectors = int(_map.get("LBA48  user addressable sectors")) \
									if "LBA48  user addressable sectors" in _map \
									else None

		self.logSectSize = _VALUE_PARSER_WITH_UNIT(_map.get("Logical  Sector size")) \
									if "Logical  Sector size" in _map \
									else None

		self.phySectSize = _VALUE_PARSER_WITH_UNIT(_map.get("Physical Sector size")) \
									if "Physical Sector size" in _map \
									else None

		self.logSectOfs = _VALUE_PARSER_WITH_UNIT(_map.get("Logical Sector-0 offset")) \
									if "Logical Sector-0 offset" in _map \
									else None

		self.totalSize = _VALUE_PARSER_WITH_UNIT(_map.get("device size with M = 1024*1024")) \
									if "device size with M = 1024*1024" in _map \
									else None

		self.formFactor = _map.get("Form Factor") \
									if "Form Factor" in _map \
									else None

		self.nominalMediaRotationRate = _map.get("Nominal Media Rotation Rate") \
									if "Nominal Media Rotation Rate" in _map \
									else None
	#

	def toJSON(self) -> dict:
		return {
			"maxLBA48Sectors": self.maxLBA48Sectors,
			"logSectSize": self.logSectSize,
			"phySectSize": self.phySectSize,
			"logSectOfs": self.logSectOfs,
			"totalSize": self.totalSize,
			"formFactor": self.formFactor,
			"nominalMediaRotationRate": self.nominalMediaRotationRate,
		}
	#

#

class _CommandsFeaturesBlock(object):

	"""
		'   *\tSMART feature set',
		'    \tSecurity Mode feature set',
		'   *\tPower Management feature set',
		'   *\tWrite cache',
		'   *\tLook-ahead',
		'   *\tWRITE_BUFFER command',
		'   *\tREAD_BUFFER command',
		'   *\tNOP cmd',
		'   *\tDOWNLOAD_MICROCODE',
		'   *\tAdvanced Power Management feature set',
		'   *\t48-bit Address feature set',
		'   *\tMandatory FLUSH_CACHE',
		'   *\tFLUSH_CACHE_EXT',
		'   *\tSMART error logging',
		'   *\tSMART self-test',
		'   *\tGeneral Purpose Logging feature set',
		'   *\tWRITE_{DMA|MULTIPLE}_FUA_EXT',
		'   *\t64-bit World wide name',
		'   *\tWRITE_UNCORRECTABLE_EXT command',
		'   *\t{READ,WRITE}_DMA_EXT_GPL commands',
		'   *\tSegmented DOWNLOAD_MICROCODE',
		'    \tunknown 119[8]',
		'   *\tGen1 signaling speed (1.5Gb/s)',
		'   *\tGen2 signaling speed (3.0Gb/s)',
		'   *\tGen3 signaling speed (6.0Gb/s)',
		'   *\tNative Command Queueing (NCQ)',
		'   *\tPhy event counters',
		'   *\tREAD_LOG_DMA_EXT equivalent to READ_LOG_EXT',
		'   *\tDMA Setup Auto-Activate optimization',
		'    \tDevice-initiated interface power management',
		'   *\tSoftware settings preservation',
		'    \tDevice Sleep (DEVSLP)',
		'   *\tSMART Command Transport (SCT) feature set',
		'   *\tSCT Features Control (AC4)',
		'   *\tSCT Data Tables (AC5)',
		'   *\tSANITIZE_ANTIFREEZE_LOCK_EXT command',
		'   *\tSANITIZE feature set',
		'   *\tCRYPTO_SCRAMBLE_EXT command',
		'   *\tBLOCK_ERASE_EXT command',
		'   *\treserved 69[3]',
		'   *\treserved 69[4]',
		'   *\treserved 69[7]',
		'   *\tDOWNLOAD MICROCODE DMA command',
		'   *\tWRITE BUFFER DMA command',
		'   *\tREAD BUFFER DMA command',
		'   *\tData Set Management TRIM supported (limit 8 blocks)',
	"""

	def __init__(self, lineGroup:_LineGroup) -> None:
		self.__data = {}

		for line in lineGroup.lines:
			parts = line.split("\t")
			assert len(parts) == 2
			partA = parts[0].strip()
			partB = parts[1].strip()
			self.__data[partB] = len(partA) > 0
	#

	def toJSON(self) -> dict:
		return self.__data
	#

#





#
#
#
def parse_hdparm_I(stdout:str, stderr:str, exitcode:int, devPath:str) -> dict:
	lineList = jk_cmdoutputparsinghelper.LineList(stdout.split("\n"))
	#lineList.dump()

	# ----------------------------------------------------------------

	# find the beginning
	nStart = lineList.findExact(devPath + ":")
	if nStart < 0:
		raise Exception("Parse error!")
	nStart += 1
	assert not lineList[nStart]		# this should be an empty line
	nStart += 1

	if len(lineList) == 3:
		return {}

	assert lineList[nStart]			# this should not be an empty line

	# find an empty line after beginning
	nEnd = lineList.findExact("", nStart)
	if nEnd < 0:
		raise Exception("Parse error!")

	# extract that part
	lineList = lineList.extractFromTo(nStart, nEnd)

	# process
	lineList.rightTrimAllLines()

	# convert to _LineGroup[]
	#print("@" * 160)
	lineGroups = []
	for lg in lineList.splitAtRows(lineList.identifyRowsNotStartingWithSpaces()):
		#lg.dump()
		#print("@" * 160)
		lineGroups.append(_LineGroup(lg))
		#lineGroups[-1].dump()

	# do we have enough groups?
	assert len(lineGroups) > 3

	# ----------------------------------------------------------------
	# now begin real parsing

	# the first block is the general block. parse it.
	generalBlock = _GeneralBlock(lineGroups[0])
	#print(generalBlock.toJSON())

	# the second block should be the block "Standards:". skip  it.
	assert lineGroups[1].title == "Standards:"

	# the third block should be the block "Configuration:". parse it.
	assert lineGroups[2].title == "Configuration:"
	driveConfigurationBlock = _DriveConfigurationBlock(lineGroups[2])
	#print(driveConfigurationBlock.toJSON())

	# the forth block should be the block "Capabilities:". skip  it.
	assert lineGroups[3].title == "Capabilities:"

	# the fifth block should be the block "Commands/features:". parse it.
	assert lineGroups[4].title == "Commands/features:"
	featuresBlock = _CommandsFeaturesBlock(lineGroups[4])
	#print(featuresBlock.toJSON())

	# skip the rest for now

	# ----------------------------------------------------------------

	return {
		"general": generalBlock.toJSON(),
		"configuration": driveConfigurationBlock.toJSON(),
		"features": featuresBlock.toJSON(),
	}
#



def where_is(c = None, programName:str = None) -> str:
	assert isinstance(programName, str)

	stdout, stderr, exitcode = run(c, "sudo /usr/bin/whereis " + programName)
	assert stdout.startswith(programName + ":")
	stdout = stdout[len(programName) + 1:].strip()
	listOfLocations = stdout.split(" ")
	for loc in listOfLocations:
		if loc.endswith("/" + programName):
			return loc
	
	raise Exception("Not installed: " + programName)
#



#
# Returns:
#
def get_hdparm_I(c = None, devPath:str = None) -> typing.Union[dict,None]:
	if not devPath:
		raise Exception("Argument 'devPath' is required!")

	programPath = where_is(None, "hdparm")

	stdout, stderr, exitcode = run(c, "sudo {} -I {}".format(programPath, devPath))
	return parse_hdparm_I(stdout, stderr, exitcode, devPath)
#















