

import re

from jk_cachefunccalls import cacheCalls

from .parsing_utils import *
from .invoke_utils import run



_parserKVPs = ParseAtFirstDelimiter(delimiter="=", valueCanBeWrappedInDoubleQuotes=True)



#
# Returns:
#
#	{
#		"distribution": "ubuntu",
#		"fullNameStr": "Ubuntu 16.04.6 LTS (Xenial Xerus)"
#		"lts": true,
#		"name": "Ubuntu"
#		"version": "16.04.6",
#		"versionID": "16.04",
#		"versionStr": "16.04.6 LTS (Xenial Xerus)",
#	}
#
def parse_etc_os_release(stdout:str, stderr:str, exitcode:int) -> dict:
	if exitcode != 0:
		raise Exception()

	data = _parserKVPs.parseLines(stdout.strip().split("\n"))
	ret = {
		"name": data["NAME"],									# "Ubuntu", "Raspbian GNU/Linux"
		"distribution": data["ID"],								# "ubuntu", "raspbian"
		"version": data["PRETTY_NAME"].split()[1],				# "16.04.6", "18.04.3", "10"
		"versionID": data["VERSION_ID"],						# "16.04", "18.04", "10"
		"versionStr": data["VERSION"],							# "16.04.6 LTS (Xenial Xerus)", "18.04.3 LTS (Bionic Beaver)", "10 (buster)"
		"lts": data["PRETTY_NAME"].endswith(" LTS"),			# True/False; might only work for Ubuntu
		"fullNameStr": data["NAME"] + " " + data["VERSION"],	# this should be the same as PRETTY_NAME
		"url": data["HOME_URL"],								# "https://www.ubuntu.com/"
	}

	m = re.match(r".+\s\(([^\)]+)\)$", ret["versionStr"])
	ret["codeName"] = m.group(1) if m else None

	return ret
#



#
# Returns:
#
#	{
#		"distribution": "ubuntu",
#		"fullNameStr": "Ubuntu 16.04.6 LTS (Xenial Xerus)"
#		"lts": true,
#		"name": "Ubuntu"
#		"version": "16.04.6",
#		"versionID": "16.04",
#		"versionStr": "16.04.6 LTS (Xenial Xerus)",
#	}
#
@cacheCalls(seconds=3, dependArgs=[0])
def get_etc_os_release(c = None) -> dict:
	stdout, stderr, exitcode = run(c, "cat /etc/os-release")
	return parse_etc_os_release(stdout, stderr, exitcode)
#










