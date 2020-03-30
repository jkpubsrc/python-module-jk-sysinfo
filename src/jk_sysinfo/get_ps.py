

import os
import re
import pwd
import grp

# TODO: eliminate the use of modules pwd and grp as this way get_ps() can not be executed remotely.
#		NOTE: we might be able implement this using data from get_user_info().

from jk_cachefunccalls import cacheCalls

from .parsing_utils import *
from .invoke_utils import run



_parserColonKVP = ParseAtFirstDelimiter(delimiter="=", valueCanBeWrappedInDoubleQuotes=True)



#
# Returns:
#
#	[
#			{
#					"args": "splash",
#					"cmd": "/sbin/init",
#					"pid": 1,
#					"ppid": 0,
#					"stat": "Ss",
#					"tty": null,
#					"uid": 0,
#					"user": "root"
#			},
#			{
#					"cmd": "[kthreadd]",
#					"pid": 2,
#					"ppid": 0,
#					"stat": "S",
#					"tty": null,
#					"uid": 0,
#					"user": "root",
#					"cwd": ....
#			},
#			{
#					"cmd": "[ksoftirqd/0]",
#					"pid": 3,
#					"ppid": 2,
#					"stat": "S",
#					"tty": null,
#					"uid": 0,
#					"user": "root",
#					"cwd": ....
#			},
#			...
#			{
#					"cmd": "bash",
#					"pid": 20144,
#					"ppid": 14839,
#					"stat": "Ss+",
#					"tty": "pts/3",
#					"uid": 1000,
#					"user": "xxxxxxxx"
#					"gid": 1000,
#					"group": "xxxxxxxx",
#					"cwd": ....
#			},
#			{
#					"args": "--spawner :1.9 /org/gtk/gvfs/exec_spaw/4",
#					"cmd": "/usr/lib/gvfs/gvfsd-computer",
#					"pid": 20292,
#					"ppid": 1,
#					"stat": "Sl",
#					"tty": null,
#					"uid": 1000,
#					"user": "xxxxxxxx"
#					"gid": 1000,
#					"group": "xxxxxxxx",
#					"cwd": ....
#			},
#			...
#			{
#					"args": "/usr/share/code/resources/app/extensions/json-language-features/server/dist/jsonServerMain --node-ipc --clientProcessId=15491",
#					"cmd": "/usr/share/code/code",
#					"pid": 29554,
#					"ppid": 15491,
#					"stat": "Sl",
#					"tty": null,
#					"uid": 1000,
#					"user": "xxxxxxxx"
#					"gid": 1000,
#					"group": "xxxxxxxx",
#					"cwd": ....
#			},
#			...
#	]
#
def parse_ps(stdout:str, stderr:str, exitcode:int) -> dict:
	if exitcode != 0:
		raise Exception()

	lines = stdout.strip().split("\n")
	lines2 = splitAtVerticalSpaceColumnsFirstLineIsHeader(lines, expectedColumnsMin=7, maxColumns=7)

	#	0	 1	 2		  3		 4		5	6
	# PPID   PID TT       STAT   UID   GID CMD

	ret = []
	for group in lines2:
		uid = int(group[4])
		gid = int(group[5])
		data = {
			"ppid": int(group[0]),
			"pid": int(group[1]),
			"tty": None if group[2] == "?" else group[2],
			"stat": group[3],
			"uid": uid,
			"gid": gid,
		}

		try:
			data["cwd"] = os.readlink("/proc/" + group[1] + "/cwd")
		except:
			pass

		pos = group[6].find(" ")
		if pos > 0:
			data["cmd"] = group[6][:pos]
			data["args"] = group[6][pos+1:]
		else:
			data["cmd"] = group[6]

		pwdEntry = pwd.getpwuid(uid)
		if pwdEntry:
			data["user"] = pwdEntry.pw_name

		grpEntry = grp.getgrgid(gid)
		if grpEntry:
			data["group"] = grpEntry.gr_name

		ret.append(data)

	return ret
#



#
# Returns:
#
#	[
#			{
#					"args": "splash",
#					"cmd": "/sbin/init",
#					"pid": 1,
#					"ppid": 0,
#					"stat": "Ss",
#					"tty": null,
#					"uid": 0,
#					"user": "root"
#			},
#			{
#					"cmd": "[kthreadd]",
#					"pid": 2,
#					"ppid": 0,
#					"stat": "S",
#					"tty": null,
#					"uid": 0,
#					"user": "root",
#					"cwd": ....
#			},
#			{
#					"cmd": "[ksoftirqd/0]",
#					"pid": 3,
#					"ppid": 2,
#					"stat": "S",
#					"tty": null,
#					"uid": 0,
#					"user": "root",
#					"cwd": ....
#			},
#			...
#			{
#					"cmd": "bash",
#					"pid": 20144,
#					"ppid": 14839,
#					"stat": "Ss+",
#					"tty": "pts/3",
#					"uid": 1000,
#					"user": "xxxxxxxx"
#					"gid": 1000,
#					"group": "xxxxxxxx",
#					"cwd": ....
#			},
#			{
#					"args": "--spawner :1.9 /org/gtk/gvfs/exec_spaw/4",
#					"cmd": "/usr/lib/gvfs/gvfsd-computer",
#					"pid": 20292,
#					"ppid": 1,
#					"stat": "Sl",
#					"tty": null,
#					"uid": 1000,
#					"user": "xxxxxxxx"
#					"gid": 1000,
#					"group": "xxxxxxxx",
#					"cwd": ....
#			},
#			...
#			{
#					"args": "/usr/share/code/resources/app/extensions/json-language-features/server/dist/jsonServerMain --node-ipc --clientProcessId=15491",
#					"cmd": "/usr/share/code/code",
#					"pid": 29554,
#					"ppid": 15491,
#					"stat": "Sl",
#					"tty": null,
#					"uid": 1000,
#					"user": "xxxxxxxx"
#					"gid": 1000,
#					"group": "xxxxxxxx",
#					"cwd": ....
#			},
#			...
#	]
#
# NOTE: This method makes use of the python modules <c>pwd</c> and <c>grp</c> which make use of the local user and group database only.
#		For that reason this function can not be executed remotely until the implementation has been improved here.
#
def get_ps(c = None) -> dict:
	stdout, stderr, exitcode = run(c, "ps ax -o ppid,pid,tty,stat,uid,gid,cmd")
	return parse_ps(stdout, stderr, exitcode)
#










