

from jk_cachefunccalls import cacheCalls

from .parsing_utils import *
from .invoke_utils import run



_parserColonKVP = ParseAtFirstDelimiter(delimiter=":", valueCanBeWrappedInDoubleQuotes=False, keysReplaceSpacesWithUnderscores=False)



#
# Requires:
#	system package "needrestart"
#
# Returns:
#
#	{
#		"kernelAfterReboot": "4.15.0-58-generic",
#		"kernelCurrent": "4.15.0-58-generic",
#		"needsReboot": true,
#		"updateKernel": false,
#		"updateMicroCodeOrABI": true
#	}
#
def parse_needs_reboot(stdout:str, stderr:str, exitcode:int) -> dict:

	"""
	NEEDRESTART-VER: 2.6
	NEEDRESTART-KCUR: 4.4.0-154-generic
	NEEDRESTART-KEXP: 4.4.0-159-generic
	NEEDRESTART-KSTA: 3
	"""

	if exitcode != 0:
		raise Exception("Not installed: needrestart")

	lines = stdout.strip().split("\n")

	d = _parserColonKVP.parseLines(lines)

	if d["NEEDRESTART-KSTA"] == "0":
		raise Exception()

	ret = {
		"needsReboot": int(d["NEEDRESTART-KSTA"]) > 1,
		"updateMicroCodeOrABI": int(d["NEEDRESTART-KSTA"]) == 2,
		"updateKernel": int(d["NEEDRESTART-KSTA"]) == 3,
	}

	if "NEEDRESTART-KCUR" in d:
		ret["kernelCurrent"] = d["NEEDRESTART-KCUR"]
	if "NEEDRESTART-KEXP" in d:
		ret["kernelAfterReboot"] = d["NEEDRESTART-KEXP"]

	return ret
#



#
# Requires:
#	system package "needrestart"
#
# Returns:
#
#	{
#		"kernelAfterReboot": "4.15.0-58-generic",
#		"kernelCurrent": "4.15.0-58-generic",
#		"needsReboot": true,
#		"updateKernel": false,
#		"updateMicroCodeOrABI": true
#	}
#
@cacheCalls(seconds=3, dependArgs=[0])
def get_needs_reboot(c = None) -> dict:
	# see: https://github.com/liske/needrestart/blob/master/README.batch.md
	try:
		stdout, stderr, exitcode = run(c, "/usr/sbin/needrestart -kb")
	except:
		# needrestart not installed!
		return {}
	return parse_needs_reboot(stdout, stderr, exitcode)
#







