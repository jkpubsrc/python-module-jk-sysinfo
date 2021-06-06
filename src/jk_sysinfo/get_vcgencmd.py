

import re
import os

from jk_cachefunccalls import cacheCalls
#import jk_json

from .parsing_utils import *
from .invoke_utils import run



_parserEqKVPs = ParseAtFirstDelimiter(delimiter="=", valueCanBeWrappedInDoubleQuotes=False)
_parserColonKVPs = ParseAtFirstDelimiter(delimiter=":", valueCanBeWrappedInDoubleQuotes=False)



#
# Returns:
#
#	{
#		"cpu": {
#			"freq_current": 500,
#			"freq_max": 1500,
#			"freq_min": 200
#		},
#		"gpu": {
#			"freq_max": 500,
#			"freq_min": 250
#		},
#		"ram": {
#			"total_mbytes": 4096
#		}
#	}
#
def _parse_vcgencmd_get_config(stdout:str, stderr:str, exitcode:int, outData:dict = None) -> dict:
	if exitcode != 0:
		raise Exception()

	data = _parserEqKVPs.parseLines(stdout.strip().split("\n"))
	#jk_json.prettyPrint(data)

	if outData is None:
		outData = {}

	if not "cpu" in outData:
		outData["cpu"] = {}

	outData["cpu"]["freq_max"] = int(data["arm_freq"])
	outData["cpu"]["freq_min"] = int(data["core_freq_min"])
	outData["cpu"]["freq_current"] = int(data["core_freq"])

	if not "gpu" in outData:
		outData["gpu"] = {}

	outData["gpu"]["freq_max"] = int(data["gpu_freq"])
	outData["gpu"]["freq_min"] = int(data["gpu_freq_min"])

	if not "ram" in outData:
		outData["ram"] = {}

	outData["ram"]["total_mbytes"] = int(data["total_mem"])

	return outData
#



#
# Returns:
#
#	{
#		"cpu": {
#			"freq_current": 500,
#			"freq_max": 1500,
#			"freq_min": 200
#		},
#		"gpu": {
#			"freq_max": 500,
#			"freq_min": 250
#		},
#		"ram": {
#			"total_mbytes": 4096
#		}
#	}
#
@cacheCalls(seconds=3, dependArgs=[0])
def get_vcgencmd_get_config(c = None, outData:dict = None) -> dict:
	stdout, stderr, exitcode = run(c, "/usr/bin/vcgencmd get_config int")
	return _parse_vcgencmd_get_config(stdout, stderr, exitcode, outData)
#



def _parse_vcgencmd_measure_volts(stdout:str, stderr:str, exitcode:int, key:str, outData:dict = None) -> dict:
	if exitcode != 0:
		raise Exception()

	data = _parserEqKVPs.parseLines(stdout.strip().split("\n"))
	#jk_json.prettyPrint(data)

	if outData is None:
		outData = {}

	if key not in outData:
		outData[key] = {}

	assert data["volt"].endswith("V")
	outData[key]["volt"] = float(data["volt"][:-1])

	return outData
#



@cacheCalls(seconds=3, dependArgs=[0])
def get_vcgencmd_measure_volts(c = None, outData:dict = None) -> dict:
	stdout, stderr, exitcode = run(c, "/usr/bin/vcgencmd measure_volts core")
	outData = _parse_vcgencmd_measure_volts(stdout, stderr, exitcode, "cpu", outData)
	stdout, stderr, exitcode = run(c, "/usr/bin/vcgencmd measure_volts sdram_c")
	outData = _parse_vcgencmd_measure_volts(stdout, stderr, exitcode, "ram", outData)
	return outData
#



def _parse_vcgencmd_measure_temp(stdout:str, stderr:str, exitcode:int, outData:dict = None) -> dict:
	if exitcode != 0:
		raise Exception()

	data = _parserEqKVPs.parseLines(stdout.strip().split("\n"))
	#jk_json.prettyPrint(data)

	if outData is None:
		outData = {}

	if not "cpu" in outData:
		outData["cpu"] = {}

	assert data["temp"].endswith("'C")
	outData["cpu"]["temp"] = float(data["temp"][:-2])

	return outData
#



@cacheCalls(seconds=3, dependArgs=[0])
def get_vcgencmd_measure_temp(c = None, outData:dict = None) -> dict:
	stdout, stderr, exitcode = run(c, "/usr/bin/vcgencmd measure_temp")
	return _parse_vcgencmd_measure_temp(stdout, stderr, exitcode, outData)
#



def _parse_vcgencmd_get_mem(stdout:str, stderr:str, exitcode:int, key:str, outData:dict = None) -> dict:
	if exitcode != 0:
		raise Exception()

	data = _parserEqKVPs.parseLines(stdout.strip().split("\n"))
	#jk_json.prettyPrint(data)
	assert len(data) == 1
	for v in data.values():
		assert v.endswith("M")
		value = int(v[:-1])
		break

	if outData is None:
		outData = {}

	if not "ram" in outData:
		outData["ram"] = {}

	outData["ram"][key] = value

	return outData
#



@cacheCalls(seconds=3, dependArgs=[0])
def get_vcgencmd_get_mem(c = None, outData:dict = None) -> dict:
	stdout, stderr, exitcode = run(c, "/usr/bin/vcgencmd get_mem arm")
	outData = _parse_vcgencmd_get_mem(stdout, stderr, exitcode, "system_mbytes", outData)
	stdout, stderr, exitcode = run(c, "/usr/bin/vcgencmd get_mem gpu")
	outData = _parse_vcgencmd_get_mem(stdout, stderr, exitcode, "gpu_mbytes", outData)
	return outData
#



def _parse_vcgencmd_display_power(stdout:str, stderr:str, exitcode:int, outData:dict = None) -> dict:
	if exitcode != 0:
		raise Exception()

	data = _parserEqKVPs.parseLines(stdout.strip().split("\n"))
	#jk_json.prettyPrint(data)
	assert len(data) == 1
	for v in data.values():
		value = int(v)
		break

	if outData is None:
		outData = {}

	if "display" not in outData:
		outData["display"] = {}

	outData["display"]["on"] = value > 0

	return outData
#



@cacheCalls(seconds=3, dependArgs=[0])
def get_vcgencmd_display_power(c = None, outData:dict = None) -> dict:
	stdout, stderr, exitcode = run(c, "/usr/bin/vcgencmd display_power")
	outData = _parse_vcgencmd_display_power(stdout, stderr, exitcode, outData)
	return outData
#



#
# Returns:
#
#	{
#		"cpu": {
#			"freq_current": 500,
#			"freq_max": 1500,
#			"freq_min": 200,
#			"temp": 36.0,
#			"volt": 0.8625
#		},
#		"display": {
#			"on": false
#		},
#		"gpu": {
#			"freq_max": 500,
#			"freq_min": 250
#		},
#		"ram": {
#			"gpu_mbytes": 76,
#			"system_mbytes": 948,
#			"total_mbytes": 4096,
#			"volt": 1.1
#		}
#	}
#
def get_vcgencmd(c = None, _ignoreCache:bool = False) -> dict:
	ret = {}
	get_vcgencmd_get_config(c, ret, _ignoreCache=_ignoreCache)
	get_vcgencmd_measure_volts(c, ret, _ignoreCache=_ignoreCache)
	get_vcgencmd_measure_temp(c, ret, _ignoreCache=_ignoreCache)
	get_vcgencmd_get_mem(c, ret, _ignoreCache=_ignoreCache)
	get_vcgencmd_display_power(c, ret, _ignoreCache=_ignoreCache)
	return ret
#



def has_local_vcgencmd() -> bool:
	# TODO: can we generalize this?
	return os.path.isfile("/usr/bin/vcgencmd")
#







