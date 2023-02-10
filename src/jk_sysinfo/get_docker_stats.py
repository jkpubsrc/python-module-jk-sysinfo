

import re
import typing
import os
import json

from .invoke_utils import run





def _parsePC(text:str) -> float:
	text = text.strip()

	m = re.match("^(([0-9]+\.[0-9]+)|0)%$", text)
	if not m:
		raise Exception("Failed to parse: " + repr(text))
	return float(m.group(1)) / 100.0
#

def _parseBytes(text:str) -> int:
	text = text.strip()
	orgText = text
	textLC = text.lower()

	factor = 1
	if textLC.endswith("kib"):
		factor = 1024
		text = text[:-3]
	elif textLC.endswith("mib"):
		factor = 1024*1024
		text = text[:-3]
	elif textLC.endswith("gib"):
		factor = 1024*1024*1024
		text = text[:-3]
	elif textLC.endswith("tib"):
		factor = 1024*1024*1024*1024
		text = text[:-3]
	elif textLC.endswith("kb"):
		factor = 1000
		text = text[:-2]
	elif textLC.endswith("mb"):
		factor = 1000000
		text = text[:-2]
	elif textLC.endswith("gb"):
		factor = 1000000000
		text = text[:-2]
	elif textLC.endswith("tb"):
		factor = 1000000000000
		text = text[:-2]
	elif textLC.endswith("b"):
		text = text[:-1]
	
	if not text or not text[-1].isnumeric():
		raise Exception("Parse error: " + repr(orgText))

	value = int(round(float(text) * factor))

	return value
#




def parse_docker_stats(stdout:str, stderr:str, exitcode:int) -> typing.List[typing.Dict[str,typing.Any]]:
	if exitcode != 0:
		raise Exception()

	ret = []

	for line in stdout.split("\n"):
		if not line:
			continue

		jData = json.loads(line)

		containerID = jData["ID"]
		name = jData["Name"]
		nPIDs = int(jData["PIDs"])
		cpuPC1 = _parsePC(jData["CPUPerc"])
		memPC1 = _parsePC(jData["MemPerc"])

		sMemUsage, sMemLimit = jData["MemUsage"].split("/")
		memUsage = _parseBytes(sMemUsage)
		memLimit = _parseBytes(sMemLimit)

		sNetIOr, sNetIOw = jData["NetIO"].split("/")
		netIOr = _parseBytes(sNetIOr)
		netIOw = _parseBytes(sNetIOw)

		sBlockIOr, sBlockIOw = jData["BlockIO"].split("/")
		blockIOr = _parseBytes(sBlockIOr)
		blockIOw = _parseBytes(sBlockIOw)

		ret.append({
			"id": containerID,
			"name": name,
			"pids": nPIDs,
			"memory": {
				"load1": memPC1,
				"usage": memUsage,
				"limit": memLimit,
			},
			"cpu": {
				"load1": cpuPC1,
			},
			"netIO": {
				"read": netIOr,
				"write": netIOw,
			},
			"blockIO": {
				"read": blockIOr,
				"write": blockIOw,
			},
		})

	return ret
#



def get_docker_stats(c = None) -> dict:
	# stdout, stderr, exitcode = run(c, "/usr/bin/docker stats --no-trunc --no-stream")
	stdout, stderr, exitcode = run(c, "/usr/bin/docker stats --no-trunc --no-stream --format '{{json .}}'")
	return parse_docker_stats(stdout, stderr, exitcode)
#



def has_local_docker() -> bool:
	# TODO: can we generalize this?
	return os.path.isfile("/usr/bin/docker")
#







