

import re

from jk_cachefunccalls import cacheCalls

from .parsing_utils import *
from .invoke_utils import run

from .get_etc_os_release import get_etc_os_release
from .get_vcgencmd import get_vcgencmd_get_config




#
# Returns:
#	{
#		"count": 4,
#		"cpus": [
#			{
#				"freq_max": 3900,
#				"freq_min": 800
#			},
#			{
#				"freq_max": 3900,
#				"freq_min": 800
#			},
#			{
#				"freq_max": 3900,
#				"freq_min": 800
#			},
#			{
#				"freq_max": 3900,
#				"freq_min": 800
#			}
#			],
#		"freq_max": 3900,
#		"freq_min": 800
#	}
#
@cacheCalls(seconds=3, dependArgs=[0])
def get_cpu_info(c = None) -> dict:
	os_release = get_etc_os_release(c)

	ret = {}

	stdout, _, _ = run(c, "/bin/ls /sys/devices/system/cpu/")
	cpus = []
	for x in stdout.strip().split():
		if x:
			if re.match(r"^cpu(\d+)$", x):
				cpus.append(x)

	ret = {
		"count": len(cpus),
		"cpus": [],
	}

	_freqMins = []			# collectors
	_freqMaxs = []			# collectors

	if os_release["distribution"] == "raspbian":
		# Raspian Linux
		_cfg_result = get_vcgencmd_get_config(c)
		freqMin = _cfg_result["cpu"]["freq_min"]
		freqMax = _cfg_result["cpu"]["freq_max"]
		ret["cpus"].append({
			"freq_min": freqMin,
			"freq_max": freqMax,
		})
		_freqMins.append(freqMin)
		_freqMaxs.append(freqMax)

	else:
		# other Linux; does not work in VMs
		try:
			for cpu in cpus:
				n = int(cpu[3:])
				stdoutMin, _, _ = run(c, "cat /sys/devices/system/cpu/cpufreq/policy" + str(n) + "/cpuinfo_min_freq")
				stdoutMax, _, _ = run(c, "cat /sys/devices/system/cpu/cpufreq/policy" + str(n) + "/cpuinfo_max_freq")
				freqMin = int(stdoutMin.strip()) // 1000
				freqMax = int(stdoutMax.strip()) // 1000
				ret["cpus"].append({
					"freq_min": freqMin,
					"freq_max": freqMax,
				})
				_freqMins.append(freqMin)
				_freqMaxs.append(freqMax)
		except:
			# TODO: maybe issue a warning here
			pass

	if _freqMins:
		ret["freq_min"] = min(_freqMins)
		ret["freq_max"] = max(_freqMaxs)
	else:
		ret["freq_min"] = 0
		ret["freq_max"] = 0

	return ret
#








