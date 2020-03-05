

from jk_cachefunccalls import cacheCalls

from .parsing_utils import *
from .invoke_utils import run



#
# Returns:
#
#	{
#		"/": {
#			"dev": "/dev/sda1",
#			"fstype2": null,
#			"mountPoint": "/",
#			"spaceFree": 167776964608,
#			"spaceTotal": 984362598400,
#			"spaceUsed": 766559354880
#		},
#		"/dev": {
#			"dev": null,
#			"fstype2": "udev",
#			"mountPoint": "/dev",
#			"spaceFree": 16295596032,
#			"spaceTotal": 16295596032,
#			"spaceUsed": 0
#		},
#		...
#		"/mounts/net/nbxxxxxxxx": {
#			"dev": "xxxxxxxx@192.168.10.16:/home/xxxxxxxx",
#			"fstype2": null,
#			"mountPoint": "/mounts/net/nbxxxxxxxx",
#			"spaceFree": 137069015040,
#			"spaceTotal": 1000948457472,
#			"spaceUsed": 812962639872
#		},
#		"/mounts/ramdisk": {
#			"dev": null,
#			"fstype2": "tmpfs",
#			"mountPoint": "/mounts/ramdisk",
#			"spaceFree": 268435456,
#			"spaceTotal": 268435456,
#			"spaceUsed": 0
#		},
#		"/run": {
#			"dev": null,
#			"fstype2": "tmpfs",
#			"mountPoint": "/run",
#			"spaceFree": 3253649408,
#			"spaceTotal": 3263557632,
#			"spaceUsed": 9908224
#		},
#		...
#	}
#
def parse_df(stdout:str, stderr:str, exitcode:int) -> dict:

	"""
	Filesystem                                                                    1K-blocks        Used   Available Use% Mounted on
	udev                                                                          15913668K          0K   15913668K   0% /dev
	tmpfs                                                                          3187068K       9648K    3177420K   1% /run
	/dev/sda1                                                                    961291600K  748571804K  163866008K  83% /
	tmpfs                                                                         15935324K     652060K   15283264K   5% /dev/shm
	tmpfs                                                                             5120K          4K       5116K   1% /run/lock
	tmpfs                                                                         15935324K          0K   15935324K   0% /sys/fs/cgroup
	tmpfs                                                                           262144K          0K     262144K   0% /mounts/ramdisk
	tmpfs                                                                          3187068K        108K    3186960K   1% /run/user/1000
	"""

	if exitcode != 0:
		raise Exception()

	lines = stdout.strip().split("\n")
	candidates = getPositionsOfWords(lines[0])
	positions = []
	for i, p in enumerate(candidates):
		if i == 0:
			continue
		for j in countDownCounter(p - 1, candidates[i-1]):
			b = isVerticalSpaceColumn(lines, j)
			if b:
				positions.append(j)
				break

	ret = {}
	for line in lines[1:]:
		data = lineSplitAt(line, positions)
		devicePathOrFileSystem, sSpaceTotal, sSpaceUsed, sSpaceFree, sUsedPerCent, mountPoint = data
		if sSpaceTotal[-1] == "K":
			sSpaceTotal = sSpaceTotal[:-1]
		if sSpaceUsed[-1] == "K":
			sSpaceUsed = sSpaceUsed[:-1]
		if sSpaceFree[-1] == "K":
			sSpaceFree = sSpaceFree[:-1]
		isDevicePath = devicePathOrFileSystem.find("/") >= 0
		devicePath = devicePathOrFileSystem if isDevicePath else None
		fstype2 = None if isDevicePath else devicePathOrFileSystem
		data = {
			"dev": devicePath,
			"fstype2": fstype2,
			"spaceTotal": int(sSpaceTotal)*1024,
			"spaceUsed": int(sSpaceUsed)*1024,
			"spaceFree": int(sSpaceFree)*1024,
			"mountPoint": mountPoint,
		}
		ret[mountPoint] = data
	return ret
#



#
# Returns:
#
#	{
#		"/": {
#			"dev": "/dev/sda1",
#			"fstype2": null,
#			"mountPoint": "/",
#			"spaceFree": 167776964608,
#			"spaceTotal": 984362598400,
#			"spaceUsed": 766559354880
#		},
#		"/dev": {
#			"dev": null,
#			"fstype2": "udev",
#			"mountPoint": "/dev",
#			"spaceFree": 16295596032,
#			"spaceTotal": 16295596032,
#			"spaceUsed": 0
#		},
#		...
#		"/mounts/net/nbxxxxxxxx": {
#			"dev": "xxxxxxxx@192.168.10.16:/home/xxxxxxxx",
#			"fstype2": null,
#			"mountPoint": "/mounts/net/nbxxxxxxxx",
#			"spaceFree": 137069015040,
#			"spaceTotal": 1000948457472,
#			"spaceUsed": 812962639872
#		},
#		"/mounts/ramdisk": {
#			"dev": null,
#			"fstype2": "tmpfs",
#			"mountPoint": "/mounts/ramdisk",
#			"spaceFree": 268435456,
#			"spaceTotal": 268435456,
#			"spaceUsed": 0
#		},
#		"/run": {
#			"dev": null,
#			"fstype2": "tmpfs",
#			"mountPoint": "/run",
#			"spaceFree": 3253649408,
#			"spaceTotal": 3263557632,
#			"spaceUsed": 9908224
#		},
#		...
#	}
#
@cacheCalls(seconds=3, dependArgs=[0])
def get_df(c = None) -> dict:
	stdout, stderr, exitcode = run(c, "/bin/df -BK")
	return parse_df(stdout, stderr, exitcode)
#


















