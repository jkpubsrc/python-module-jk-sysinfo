


import os

from jk_cachefunccalls import cacheCalls

from .parsing_utils import *
from .invoke_utils import run



_parserColonKVP = ParseAtFirstDelimiter(delimiter=":", valueCanBeWrappedInDoubleQuotes=False, keysReplaceSpacesWithUnderscores=False)




#
# Requires:
#	system package "sensors"
#
# Returns:
#	{
#		"acpitz-virtual-0": {
#			"adapterType": "Virtual device",
#			"device": "acpitz-virtual-0",
#			"sensorData": {
#				"temp1": {
#					"crit": 119.0,
#					"value": 27.8
#				},
#				"temp2": {
#					"crit": 119.0,
#					"value": 29.8
#				}
#			}
#		},
#		"coretemp-isa-0000": {
#			"adapterType": "ISA adapter",
#			"device": "coretemp-isa-0000",
#			"sensorData": {
#				"Core_0": {
#					"crit": 100.0,
#					"crit_alarm": 0.0,
#					"value": 27.0,
#					"max": 84.0
#				},
#				"Core_1": {
#					"crit": 100.0,
#					"crit_alarm": 0.0,
#					"value": 27.0,
#					"max": 84.0
#				},
#				"Core_2": {
#					"crit": 100.0,
#					"crit_alarm": 0.0,
#					"value": 25.0,
#					"max": 84.0
#				},
#				"Core_3": {
#					"crit": 100.0,
#					"crit_alarm": 0.0,
#					"value": 23.0,
#					"max": 84.0
#				},
#				"Physical_id_0": {
#					"crit": 100.0,
#					"crit_alarm": 0.0,
#					"value": 29.0,
#					"max": 84.0
#				}
#			}
#		}
#	}
#
# Notes:
# * Some WLAN adapters have a temperature sensor. If WLAN is turned off no value will be measured. Therefor a sensor data dictionary can be empty and will have no <c>value</c> key.
#
def parse_sensors(stdout:str, stderr:str, exitcode:int) -> dict:

	"""
	acpitz-virtual-0
	Adapter: Virtual device
	temp1:
	  temp1_input: 27.800
	  temp1_crit: 119.000
	temp2:
	  temp2_input: 29.800
	  temp2_crit: 119.000

	coretemp-isa-0000
	Adapter: ISA adapter
	Physical id 0:
	  temp1_input: 26.000
	  temp1_max: 84.000
	  temp1_crit: 100.000
	  temp1_crit_alarm: 0.000
	Core 0:
	  temp2_input: 24.000
	  temp2_max: 84.000
	  temp2_crit: 100.000
	  temp2_crit_alarm: 0.000
	Core 1:
	  temp3_input: 24.000
	  temp3_max: 84.000
	  temp3_crit: 100.000
	  temp3_crit_alarm: 0.000
	Core 2:
	  temp4_input: 23.000
	  temp4_max: 84.000
	  temp4_crit: 100.000
	  temp4_crit_alarm: 0.000
	Core 3:
	  temp5_input: 23.000
	  temp5_max: 84.000
	  temp5_crit: 100.000
	  temp5_crit_alarm: 0.000
	"""

	if exitcode != 0:
		raise Exception()

	lines = stdout.strip().split("\n")

	ret = {}
	for lineGroup in splitAtEmptyLines(lines):
		device = lineGroup[0]
		adapterType = lineGroup[1].split(":")[1].strip()
		sensorData = groupLinesByLeadingSpace(lineGroup[2:])

		sensorData2 = {}
		for sensorName, vGroup in sensorData.items():
			assert sensorName.endswith(":")
			sensorName = sensorName[:-1].replace(" ", "_")
			sensorData3 = {}
			for vkey, vValue in _parserColonKVP.parseLines(vGroup).items():
				if vkey.startswith("temp"):
					sensorData3["sensor"] = "temp"
					pos = vkey.find("_")
					vkey = vkey[pos+1:]
				elif vkey.startswith("fan"):
					sensorData3["sensor"] = "fan"
					pos = vkey.find("_")
					vkey = vkey[pos+1:]
				if vkey == "input":
					vkey = "value"
				sensorData3[vkey] = float(vValue)
			sensorData2[sensorName] = sensorData3

		ret[device] = {
			"device": device,
			"adapterType": adapterType,
			"sensorData": sensorData2,
		}

	return ret
#



#
# Requires:
#	system package "sensors"
#
# Returns:
#	{
#		"acpitz-virtual-0": {
#			"adapterType": "Virtual device",
#			"device": "acpitz-virtual-0",
#			"sensorData": {
#				"temp1": {
#					"crit": 119.0,
#					"value": 27.8
#				},
#				"temp2": {
#					"crit": 119.0,
#					"value": 29.8
#				}
#			}
#		},
#		"coretemp-isa-0000": {
#			"adapterType": "ISA adapter",
#			"device": "coretemp-isa-0000",
#			"sensorData": {
#				"Core_0": {
#					"crit": 100.0,
#					"crit_alarm": 0.0,
#					"value": 27.0,
#					"max": 84.0
#				},
#				"Core_1": {
#					"crit": 100.0,
#					"crit_alarm": 0.0,
#					"value": 27.0,
#					"max": 84.0
#				},
#				"Core_2": {
#					"crit": 100.0,
#					"crit_alarm": 0.0,
#					"value": 25.0,
#					"max": 84.0
#				},
#				"Core_3": {
#					"crit": 100.0,
#					"crit_alarm": 0.0,
#					"value": 23.0,
#					"max": 84.0
#				},
#				"Physical_id_0": {
#					"crit": 100.0,
#					"crit_alarm": 0.0,
#					"value": 29.0,
#					"max": 84.0
#				}
#			}
#		}
#	}
#
def get_sensors(c = None) -> dict:
	stdout, stderr, exitcode = run(c, "/usr/bin/sensors -u")
	return parse_sensors(stdout, stderr, exitcode)
#



def has_local_sensors() -> bool:
	# TODO: can we generalize this?
	return os.path.isfile("/usr/bin/sensors")
#







