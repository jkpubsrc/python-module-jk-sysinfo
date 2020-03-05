

from jk_cachefunccalls import cacheCalls

from .parsing_utils import *
from .invoke_utils import run



#
# Returns:
#
#	{
#		"load1": 0.13,
#		"load15": 0.29,
#		"load5": 0.3,
#		"processes_total": 1052,
#		"processes_runnable": 1
#	}
#
def parse_proc_load_avg(stdout:str, stderr:str, exitcode:int) -> dict:

	"""
	0.12 0.22 0.25 1/1048 16989
	"""

	if exitcode != 0:
		raise Exception()

	ret = stdout.strip().split(" ")
	return {
		"load1": float(ret[0]),
		"load5": float(ret[1]),
		"load15": float(ret[2]),
		"processes_runnable": int(ret[3].split("/")[0]),
		"processes_total": int(ret[3].split("/")[1]),
	}
#



#
# Returns:
#
#	{
#		"load1": 0.13,
#		"load15": 0.29,
#		"load5": 0.3,
#		"processes_total": 1052,
#		"processes_runnable": 1
#	}
#
def get_proc_load_avg(c = None) -> dict:
	stdout, stderr, exitcode = run(c, "cat /proc/loadavg")
	return parse_proc_load_avg(stdout, stderr, exitcode)
#















