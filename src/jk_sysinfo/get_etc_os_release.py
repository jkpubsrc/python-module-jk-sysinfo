

from .parsing_utils import *
from .invoke_utils import run



_parserColonKVP = ParseAtFirstDelimiter(delimiter="=", valueCanBeWrappedInDoubleQuotes=True)



#
# Returns:
#
#	{
#		"distribution": "ubuntu",
#		"lts": true,
#		"version": "16.04.6"
#	}
#
def parse_etc_os_release(stdout:str, stderr:str, exitcode:int) -> dict:

	"""
	NAME="Ubuntu"
	VERSION="16.04.6 LTS (Xenial Xerus)"
	ID=ubuntu
	ID_LIKE=debian
	PRETTY_NAME="Ubuntu 16.04.6 LTS"
	VERSION_ID="16.04"
	HOME_URL="http://www.ubuntu.com/"
	SUPPORT_URL="http://help.ubuntu.com/"
	BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
	VERSION_CODENAME=xenial
	UBUNTU_CODENAME=xenial
	"""

	if exitcode != 0:
		raise Exception()

	ret = _parserColonKVP.parseLines(stdout.strip().split("\n"))
	return {
		"distribution": ret["ID"],
		"version": ret["PRETTY_NAME"].split()[1],
		"lts": ret["PRETTY_NAME"].endswith(" LTS"),
	}
#



#
# Returns:
#
#	{
#		"distribution": "ubuntu",
#		"lts": true,
#		"version": "16.04.6"
#	}
#
def get_etc_os_release(c = None) -> dict:
	stdout, stderr, exitcode = run(c, "cat /etc/os-release")
	return parse_etc_os_release(stdout, stderr, exitcode)
#










