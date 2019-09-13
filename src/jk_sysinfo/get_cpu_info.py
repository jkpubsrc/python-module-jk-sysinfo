

import re

from .parsing_utils import *
from .invoke_utils import run






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
def get_cpu_info(c = None) -> dict:
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

	totalFreqMin = 999999999999999
	totalFreqMax = 0
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
		if freqMax > totalFreqMax:
			totalFreqMax = freqMax
		if freqMin < totalFreqMin:
			totalFreqMin = freqMin

	ret["freq_min"] = totalFreqMin
	ret["freq_max"] = totalFreqMax

	return ret
#







