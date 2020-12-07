

import collections


OSInfo = collections.namedtuple("OSInfo", [
	"class",
	"distribution",
	
])








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









