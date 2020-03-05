

import re

from jk_cachefunccalls import cacheCalls

from .parsing_utils import *
from .invoke_utils import run



#
# Returns:
#
#	{
#		"/sys": {
#				"dev": null,
#				"fstype": "sysfs",
#				"fstype2": "sysfs",
#				"mountPoint": "/sys",
#				"options": [
#						"rw",
#						"nosuid",
#						"nodev",
#						"noexec",
#						"relatime"
#				]
#		},
#		"/proc": {
#				"dev": null,
#				"fstype": "proc",
#				"fstype2": "proc",
#				"mountPoint": "/proc",
#				"options": [
#						"rw",
#						"nosuid",
#						"nodev",
#						"noexec",
#						"relatime"
#				]
#		},
#		"/dev": {
#				"dev": null,
#				"fstype": "devtmpfs",
#				"fstype2": "udev",
#				"mountPoint": "/dev",
#				"options": [
#						"rw",
#						"nosuid",
#						"relatime",
#						"size=15913668k",
#						"nr_inodes=3978417",
#						"mode=755"
#				]
#		},
#		...,
#		"/run": {
#				"dev": null,
#				"fstype": "tmpfs",
#				"fstype2": "tmpfs",
#				"mountPoint": "/run",
#				"options": [
#						"rw",
#						"nosuid",
#						"noexec",
#						"relatime",
#						"size=3187068k",
#						"mode=755"
#				]
#		},
#		...,
#		"/mounts/net/nbxxxxxxxx": {
#				"dev": "xxxxxxxx@192.168.10.16:/home/xxxxxxxx",
#				"fstype": "fuse.sshfs",
#				"fstype2": null,
#				"mountPoint": "/mounts/net/nbxxxxxxxx",
#				"options": [
#						"rw",
#						"nosuid",
#						"nodev",
#						"relatime",
#						"user_id=1000",
#						"group_id=1000",
#						"allow_other"
#				]
#		},
#		...
#	}
#
def parse_mount(stdout:str, stderr:str, exitcode:int) -> dict:

	"""
	sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)
	proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
	udev on /dev type devtmpfs (rw,nosuid,relatime,size=8018528k,nr_inodes=2004632,mode=755)
	devpts on /dev/pts type devpts (rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000)
	tmpfs on /run type tmpfs (rw,nosuid,noexec,relatime,size=1608252k,mode=755)
	/dev/sdb1 on / type ext4 (rw,relatime,errors=remount-ro,data=ordered)
	...
	"""

	if exitcode != 0:
		raise Exception()

	lines = stdout.strip().split("\n")

	ret = {}
	for line in lines:
		m = re.match(r"^(.+?) on (.+?) type ([^\s]+) \(([^\s]+)\)$", line)
		if m is None:
			raise Exception("Failed to parse line: " + repr(line))

		groups = m.groups()
		devicePathOrFileSystem = groups[0]
		mountPoint = groups[1]
		fstype = groups[2]
		mountOptions = groups[3].split(",")
		isDevicePath = devicePathOrFileSystem.find("/") >= 0
		devicePath = devicePathOrFileSystem if isDevicePath else None
		fstype2 = None if isDevicePath else devicePathOrFileSystem
		ret[mountPoint] = {
			"dev": devicePath,
			"fstype": fstype,
			"fstype2": fstype2,
			"options": mountOptions,
			"mountPoint": mountPoint,
		}

	return ret
#



#
# Returns:
#
#	{
#		"/sys": {
#				"dev": null,
#				"fstype": "sysfs",
#				"fstype2": "sysfs",
#				"mountPoint": "/sys",
#				"options": [
#						"rw",
#						"nosuid",
#						"nodev",
#						"noexec",
#						"relatime"
#				]
#		},
#		"/proc": {
#				"dev": null,
#				"fstype": "proc",
#				"fstype2": "proc",
#				"mountPoint": "/proc",
#				"options": [
#						"rw",
#						"nosuid",
#						"nodev",
#						"noexec",
#						"relatime"
#				]
#		},
#		"/dev": {
#				"dev": null,
#				"fstype": "devtmpfs",
#				"fstype2": "udev",
#				"mountPoint": "/dev",
#				"options": [
#						"rw",
#						"nosuid",
#						"relatime",
#						"size=15913668k",
#						"nr_inodes=3978417",
#						"mode=755"
#				]
#		},
#		...,
#		"/run": {
#				"dev": null,
#				"fstype": "tmpfs",
#				"fstype2": "tmpfs",
#				"mountPoint": "/run",
#				"options": [
#						"rw",
#						"nosuid",
#						"noexec",
#						"relatime",
#						"size=3187068k",
#						"mode=755"
#				]
#		},
#		...,
#		"/mounts/net/nbxxxxxxxx": {
#				"dev": "xxxxxxxx@192.168.10.16:/home/xxxxxxxx",
#				"fstype": "fuse.sshfs",
#				"fstype2": null,
#				"mountPoint": "/mounts/net/nbxxxxxxxx",
#				"options": [
#						"rw",
#						"nosuid",
#						"nodev",
#						"relatime",
#						"user_id=1000",
#						"group_id=1000",
#						"allow_other"
#				]
#		},
#		...
#	}
#
@cacheCalls(seconds=3, dependArgs=[0])
def get_mount(c = None) -> dict:
	stdout, stderr, exitcode = run(c, "/bin/mount")
	return parse_mount(stdout, stderr, exitcode)
#


















