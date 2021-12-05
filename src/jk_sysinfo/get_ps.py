

import os
import re
import pwd
import grp
import typing
import resource

# TODO: eliminate the use of modules pwd and grp as this way get_ps() can not be executed remotely.
#		NOTE: we might be able implement this using data from get_user_info().

from jk_cachefunccalls import cacheCalls
import jk_cmdoutputparsinghelper

from .parsing_utils import *
from .invoke_utils import run

_PAGESIZE = resource.getpagesize()
_PAGESIZE_KB = _PAGESIZE / 1024


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
def parse_ps(stdout:str, stderr:str, exitcode:int, userIDToNameMap:typing.Dict[int,str] = None, grpIDToNameMap:typing.Dict[int,str] = None) -> dict:
	if exitcode != 0:
		raise Exception()

	lines = jk_cmdoutputparsinghelper.TextData(stdout).lines
	lines.removeTrailingEmptyLines()
	splitPositions = lines.identifySpaceColumnPositions(maxSplitPositions=6)
	table = lines.createDataTableFromColumns(positions=splitPositions, bLStrip=True, bRStrip=True, bFirstLineIsHeader=True, columnDefs=[
		jk_cmdoutputparsinghelper.ColumnDef("ppid", int),
		jk_cmdoutputparsinghelper.ColumnDef("pid", int),
		jk_cmdoutputparsinghelper.ColumnDef("tty", str),
		jk_cmdoutputparsinghelper.ColumnDef("stat", str),
		jk_cmdoutputparsinghelper.ColumnDef("uid", int),
		jk_cmdoutputparsinghelper.ColumnDef("gid", int),
		jk_cmdoutputparsinghelper.ColumnDef("cmd", str),
	])

	#	0	 1	 2		  3		 4		5	6
	# PPID   PID TT       STAT   UID   GID CMD

	ret = []
	for data in table.rowDictIterator():
		if data["tty"] == "?":
			data["tty"] = None

		try:
			# NOTE: this can only be read by root
			data["cwd"] = os.readlink("/proc/" + data["pid"] + "/cwd")
		except:
			pass

		_cmd = data["cmd"]
		pos = _cmd.find(" ")
		if pos > 0:
			data["cmd"] = _cmd[:pos]
			data["args"] = _cmd[pos+1:]

		if userIDToNameMap:
			data["user"] = userIDToNameMap.get(data["uid"], None)
		if grpIDToNameMap:
			data["group"] = grpIDToNameMap.get(data["gid"], None)

		ret.append(data)

	return ret
#



def _enrichWithVMSize(jProgramData:dict, pid:int):
	procPath = "/proc/" + str(jProgramData["pid"]) + "/statm"
	try:
		with open(procPath, "r") as f:
			components = f.read().strip().split(" ")
		assert len(components) == 7
		jProgramData["vmsizeKB"] = int(components[0]) * _PAGESIZE_KB
	except:
		jProgramData["vmsizeKB"] = -1
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
def get_ps(c = None, bAddVMemSize:bool = False, userIDToNameMap:typing.Dict[int,str] = None, grpIDToNameMap:typing.Dict[int,str] = None) -> typing.List[dict]:
	stdout, stderr, exitcode = run(c, "ps ax -o ppid,pid,tty,stat,uid,gid,cmd")

	if c is None:
		if userIDToNameMap is None:
			userIDToNameMap = {}
			for entry in pwd.getpwall():
				userIDToNameMap[entry.pw_uid] = entry.pw_name
		if grpIDToNameMap is None:
			grpIDToNameMap = {}
			for entry in grp.getgrall():
				grpIDToNameMap[entry.gr_gid] = entry.gr_name

	ret = parse_ps(stdout, stderr, exitcode, userIDToNameMap, grpIDToNameMap)

	# remove ps process information itself and enrich this data
	ret2 = []
	for jProgramData in ret:
		if (jProgramData["cmd"] in [ "ps", "/bin/sh" ]) and (jProgramData["args"].find("ax -o ppid,pid,tty,stat,uid,gid,cmd") >= 0):
			continue
		if bAddVMemSize:
			_enrichWithVMSize(jProgramData, jProgramData["pid"])
		ret2.append(jProgramData)

	return ret2
#





