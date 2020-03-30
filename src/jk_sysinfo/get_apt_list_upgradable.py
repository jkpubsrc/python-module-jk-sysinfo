

import re

from jk_cachefunccalls import cacheCalls

from .parsing_utils import *
from .invoke_utils import run



#
# Returns:
#
#	{
#		"install": [
#			"containerd",
#			"linux-headers-4.4.0-159",
#			"linux-headers-4.4.0-159-generic",
#			"linux-image-4.4.0-159-generic",
#			"linux-modules-4.4.0-159-generic",
#			"linux-modules-extra-4.4.0-159-generic",
#			"runc"
#		],
#		"remove": [],
#		"unnecessary": [],
#		"upgrade": [
#			"apparmor",
#			"apport",
#			"apport-gtk",
#			"apt",
#			...
#		]
#	}
#
def parse_apt_list_upgradable(stdout:str, stderr:str, exitcode:int) -> dict:

	"""
	chromium-browser/xenial-updates,xenial-security 77.0.3865.90-0ubuntu0.16.04.1 amd64 [upgradable from: 76.0.3809.100-0ubuntu0.16.04.1]
	chromium-browser-l10n/xenial-updates,xenial-updates,xenial-security,xenial-security 77.0.3865.90-0ubuntu0.16.04.1 all [upgradable from: 76.0.3809.100-0ubuntu0.16.04.1]
	chromium-codecs-ffmpeg-extra/xenial-updates,xenial-security 77.0.3865.90-0ubuntu0.16.04.1 amd64 [upgradable from: 76.0.3809.100-0ubuntu0.16.04.1]
	e2fslibs/xenial-updates,xenial-security 1.42.13-1ubuntu1.1 amd64 [upgradable from: 1.42.13-1ubuntu1]
	e2fsprogs/xenial-updates,xenial-security 1.42.13-1ubuntu1.1 amd64 [upgradable from: 1.42.13-1ubuntu1]
	initramfs-tools/xenial-updates,xenial-updates 0.122ubuntu8.15 all [upgradable from: 0.122ubuntu8.14]
	initramfs-tools-bin/xenial-updates 0.122ubuntu8.15 amd64 [upgradable from: 0.122ubuntu8.14]
	initramfs-tools-core/xenial-updates,xenial-updates 0.122ubuntu8.15 all [upgradable from: 0.122ubuntu8.14]
	libcomerr2/xenial-updates,xenial-security 1.42.13-1ubuntu1.1 amd64 [upgradable from: 1.42.13-1ubuntu1]
	libsdl2-2.0-0/xenial-updates,xenial-security 2.0.4+dfsg1-2ubuntu2.16.04.2 amd64 [upgradable from: 2.0.4+dfsg1-2ubuntu2.16.04.1]
	libsdl2-dev/xenial-updates,xenial-security 2.0.4+dfsg1-2ubuntu2.16.04.2 amd64 [upgradable from: 2.0.4+dfsg1-2ubuntu2.16.04.1]
	libss2/xenial-updates,xenial-security 1.42.13-1ubuntu1.1 amd64 [upgradable from: 1.42.13-1ubuntu1]
	linux-generic/xenial-updates,xenial-security 4.4.0.165.173 amd64 [upgradable from: 4.4.0.164.172]
	linux-headers-generic/xenial-updates,xenial-security 4.4.0.165.173 amd64 [upgradable from: 4.4.0.164.172]
	linux-image-generic/xenial-updates,xenial-security 4.4.0.165.173 amd64 [upgradable from: 4.4.0.164.172]
	linux-libc-dev/xenial-updates,xenial-security 4.4.0-165.193 amd64 [upgradable from: 4.4.0-164.192]
	tzdata/xenial-updates,xenial-updates,xenial-security,xenial-security 2019c-0ubuntu0.16.04 all [upgradable from: 2019b-0ubuntu0.16.04]
	"""
	
	if exitcode != 0:
		raise Exception()

	lines = stdout.strip().split("\n")

	upgradable = []
	for line in lines:
		m = re.match(r"^([^/]+)/([^\s]+)\s.*\[upgradable from: .*]$", line)
		if m:
			upgradable.append(m.group(1))
		else:
			if line == "Listing...":
				continue
			else:
				raise Exception("Unparsable line: " + repr(line))

	return {
		"install": [],
		"remove": [],
		"unnecessary": [],
		"upgrade": upgradable,
	}
#



#
# Returns:
#
#	{
#		"install": [],
#		"remove": [],
#		"unnecessary": [],
#		"upgrade": [
#			"containerd",
#			"linux-headers",
#			"linux-headers-generic",
#			"linux-image-generic",
#			"linux-modules-generic",
#			"linux-modules-extra-generic",
#			"runc"
#			"apparmor",
#			"apport",
#			"apport-gtk",
#			"apt",
#			...
#		]
#	}
#
@cacheCalls(seconds=3, dependArgs=[0])
def get_apt_list_upgradable(c = None) -> dict:
	stdout, stderr, exitcode = run(c, "/usr/bin/apt list --upgradable")
	return parse_apt_list_upgradable(stdout, stderr, exitcode)
#


















