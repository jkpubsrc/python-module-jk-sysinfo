

import re

from jk_cachefunccalls import cacheCalls

from .parsing_utils import *
from .invoke_utils import run



#
# Returns:
#
#	{
#		...
#		"defusedxml": "0.6.0",
#		"dnspython": "1.16.0",
#		"docutils": "0.14",
#		...
#	}
#
def parse_pip3_list(stdout:str, stderr:str, exitcode:int) -> dict:

	"""
	...
	cymem (2.0.3)
	decorator (4.4.1)
	defer (1.0.6)
	defusedxml (0.6.0)
	distro-info (0.18ubuntu0.18.04.1)
	dnspython (1.16.0)
	docutils (0.14)
	...
	"""

	if exitcode != 0:
		raise Exception()

	ret = {}

	lines = stdout.strip().split("\n")
	for line in lines:
		m = re.match("^(.*)\s+\((.*)\)$", line)
		if m is None:
			raise Exception("Failed to parse line: " + repr(line))
		pythonPackageName = m.group(1)
		sPythonPackageVersion = m.group(2)
		ret[pythonPackageName] = sPythonPackageVersion

	return ret
#



#
# Returns:
#
#	{
#		...
#		"defusedxml": "0.6.0",
#		"dnspython": "1.16.0",
#		"docutils": "0.14",
#		...
#	}
#
#@cacheCalls(seconds=3, dependArgs=[0])
@cacheCalls(seconds=3)
def get_pip3_list(c = None) -> dict:
	stdout, stderr, exitcode = run(c, "/usr/bin/pip3 list")
	return parse_pip3_list(stdout, stderr, exitcode)
#


















