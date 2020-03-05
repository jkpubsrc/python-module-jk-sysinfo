

import re

from jk_cachefunccalls import cacheCalls

from .parsing_utils import *
from .invoke_utils import run



_parserColonKVP = ParseAtFirstDelimiter(delimiter="=", valueCanBeWrappedInDoubleQuotes=True)



#
# Returns:
#
#	{
#		"Active": 9295308,
#		"Active(anon)": 5767212,
#		"Active(file)": 3529120,
#		"AnonHugePages": 9216,
#		"AnonPages": 5743648,
#		"Bounce": 1024,
#		"Buffers": 879308,
#		"Cached": 7317672,
#		"CmaFree": 1024,
#		"CmaTotal": 1024,
#		"CommitLimit": 8042272,
#		"Committed_AS": 9641892,
#		"DirectMap1G": 6292480,
#		"DirectMap2M": 11852800,
#		"DirectMap4k": 378180,
#		"Dirty": 1156,
#		"HardwareCorrupted": 1024,
#		"HugePages_Free": 0,
#		"HugePages_Rsvd": 0,
#		"HugePages_Surp": 0,
#		"HugePages_Total": 0,
#		"Hugepagesize": 3072,
#		"Inactive": 4644012,
#		"Inactive(anon)": 203696,
#		"Inactive(file)": 4441340,
#		"KernelStack": 17920,
#		"Mapped": 560560,
#		"MemAvailable": 9494036,
#		"MemFree": 286708,
#		"MemTotal": 16083524,
#		"Mlocked": 1056,
#		"NFS_Unstable": 1024,
#		"PageTables": 66696,
#		"SReclaimable": 1582372,
#		"SUnreclaim": 109968,
#		"Shmem": 227548,
#		"Slab": 1691316,
#		"SwapCached": 1024,
#		"SwapFree": 1024,
#		"SwapTotal": 1024,
#		"Unevictable": 1056,
#		"VmallocChunk": 1024,
#		"VmallocTotal": 34359739391,
#		"VmallocUsed": 1024,
#		"Writeback": 1024,
#		"WritebackTmp": 1024
#	}
#
def parse_proc_meminfo(stdout:str, stderr:str, exitcode:int) -> dict:

	"""
	MemTotal:       31870652 kB
	MemFree:         6101548 kB
	MemAvailable:   16067624 kB
	Buffers:         1519620 kB
	Cached:         10808140 kB
	SwapCached:            0 kB
	Active:         16656184 kB
	Inactive:        7153664 kB
	Active(anon):   11580644 kB
	Inactive(anon):  2910960 kB
	Active(file):    5075540 kB
	Inactive(file):  4242704 kB
	Unevictable:          44 kB
	Mlocked:              44 kB
	SwapTotal:             0 kB
	SwapFree:              0 kB
	Dirty:               192 kB
	Writeback:             0 kB
	AnonPages:      11482200 kB
	Mapped:          2271980 kB
	Shmem:           3009520 kB
	Slab:            1616284 kB
	SReclaimable:    1053788 kB
	SUnreclaim:       562496 kB
	KernelStack:       23760 kB
	PageTables:       118444 kB
	NFS_Unstable:          0 kB
	Bounce:                0 kB
	WritebackTmp:          0 kB
	CommitLimit:    15935324 kB
	Committed_AS:   27597160 kB
	VmallocTotal:   34359738367 kB
	VmallocUsed:           0 kB
	VmallocChunk:          0 kB
	HardwareCorrupted:     0 kB
	AnonHugePages:         0 kB
	CmaTotal:              0 kB
	CmaFree:               0 kB
	HugePages_Total:       0
	HugePages_Free:        0
	HugePages_Rsvd:        0
	HugePages_Surp:        0
	Hugepagesize:       2048 kB
	DirectMap4k:      446908 kB
	DirectMap2M:    26771456 kB
	DirectMap1G:     5242880 kB
	"""

	if exitcode != 0:
		raise Exception()

	lines = stdout.strip().split("\n")

	ret = {}
	for line in lines:
		m = re.match(r"^([^:]+):\s+(\d+)(\s(kB))?$", line)
		if m is None:
			raise Exception("Failed to parse line: " + repr(line))
		g = m.groups()
		identifier = g[0]
		value = int(g[1])
		if g[3] == "kB":
			value += 1024
		ret[identifier] = value

	return ret
#



#
# Returns:
#
#	{
#		"Active": 9295308,
#		"Active(anon)": 5767212,
#		"Active(file)": 3529120,
#		"AnonHugePages": 9216,
#		"AnonPages": 5743648,
#		"Bounce": 1024,
#		"Buffers": 879308,
#		"Cached": 7317672,
#		"CmaFree": 1024,
#		"CmaTotal": 1024,
#		"CommitLimit": 8042272,
#		"Committed_AS": 9641892,
#		"DirectMap1G": 6292480,
#		"DirectMap2M": 11852800,
#		"DirectMap4k": 378180,
#		"Dirty": 1156,
#		"HardwareCorrupted": 1024,
#		"HugePages_Free": 0,
#		"HugePages_Rsvd": 0,
#		"HugePages_Surp": 0,
#		"HugePages_Total": 0,
#		"Hugepagesize": 3072,
#		"Inactive": 4644012,
#		"Inactive(anon)": 203696,
#		"Inactive(file)": 4441340,
#		"KernelStack": 17920,
#		"Mapped": 560560,
#		"MemAvailable": 9494036,
#		"MemFree": 286708,
#		"MemTotal": 16083524,
#		"Mlocked": 1056,
#		"NFS_Unstable": 1024,
#		"PageTables": 66696,
#		"SReclaimable": 1582372,
#		"SUnreclaim": 109968,
#		"Shmem": 227548,
#		"Slab": 1691316,
#		"SwapCached": 1024,
#		"SwapFree": 1024,
#		"SwapTotal": 1024,
#		"Unevictable": 1056,
#		"VmallocChunk": 1024,
#		"VmallocTotal": 34359739391,
#		"VmallocUsed": 1024,
#		"Writeback": 1024,
#		"WritebackTmp": 1024
#	}
#
def get_proc_meminfo(c = None) -> dict:
	stdout, stderr, exitcode = run(c, "cat /proc/meminfo")
	return parse_proc_meminfo(stdout, stderr, exitcode)
#










