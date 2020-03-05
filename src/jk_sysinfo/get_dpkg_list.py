

import re

from jk_cachefunccalls import cacheCalls

from .parsing_utils import *
from .invoke_utils import run

from jk_version import Version




#
# Returns:
#
#	{
#		...
#		"netcat-openbsd": "1.105-7ubuntu1",
#		"netpbm": "2:10.0-15.3",
#		"nettle-dev", "3.2-1ubuntu0.16.04.1",
#		...
#	}
#
def parse_dpkg_list(stdout:str, stderr:str, exitcode:int) -> dict:

	"""
	...
	netcat-openbsd\t1.105-7ubuntu1
	netpbm\t2:10.0-15.3
	nettle-dev\t3.2-1ubuntu0.16.04.1
	...
	"""
	
	if exitcode != 0:
		raise Exception()

	lines = stdout.strip().split("\n")

	ret = {}
	for line in lines:
		name, version = line.split("\t")
		p = name.find(":")
		if p > 0:
			name = name[:p]
		ret[name] = version

	return ret
#



#
# Returns:
#
#	{
#		...
#		"netcat-openbsd": "1.105-7ubuntu1",
#		"netpbm": "2:10.0-15.3",
#		"nettle-dev", "3.2-1ubuntu0.16.04.1",
#		...
#	}
#
@cacheCalls(seconds=3, dependArgs=[0])
def get_dpkg_list(c = None) -> dict:
	stdout, stderr, exitcode = run(c, "/usr/bin/dpkg-query -W")
	return parse_dpkg_list(stdout, stderr, exitcode)
#


















