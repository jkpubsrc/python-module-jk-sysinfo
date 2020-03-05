

from jk_cachefunccalls import cacheCalls

from .parsing_utils import *
from .invoke_utils import run



_parserColonKVP = ParseAtFirstDelimiter()



#
# Returns:
#
#	{
#		"distribution": "ubuntu",
#		"lts": true,
#		"version": "16.04.6"
#	}
#
def parse_lsb_release_a(stdout:str, stderr:str, exitcode:int) -> dict:

	if exitcode != 0:
		raise Exception()

	ret = _parserColonKVP.parseLines(stdout.split("\n"))
	return {
		"version": ret["Description"].split()[1],
		"lts": ret["Description"].endswith(" LTS"),
		"distribution": ret["Distributor ID"].lower(),
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
@cacheCalls(seconds=3, dependArgs=[0])
def get_lsb_release_a(c = None) -> dict:
	stdout, stderr, exitcode = run(c, "/usr/bin/lsb_release -a")
	return parse_lsb_release_a(stdout, stderr, exitcode)
#












