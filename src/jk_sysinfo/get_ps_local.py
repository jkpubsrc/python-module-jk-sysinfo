

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




def get_process_info_local(pid:int, userIDToNameMap:typing.Dict[int,str] = None, grpIDToNameMap:typing.Dict[int,str] = None):
	dirPath = "/proc/" + str(pid)

	#### /proc/????/status ####

	_fullContent = None
	try:
		with open(os.path.join(dirPath, "status"), "r") as f:
			_fullContent = f.read()
	except:
		return

	_pre_map = {}
	for line in _fullContent.split("\n"):
		if not line:
			continue
		m = re.match("^([a-zA-Z_]+):\s+(.+)$", line)
		if m is None:
			print("ERROR: Failed to parse line: " + line)
			return
		_pre_map[m.group(1)] = m.group(2)

	xxProcName = _pre_map["Name"]
	_sStateTemp = _pre_map["State"]
	m = re.match("^(.*)\s+\((.*)\)$", _sStateTemp)
	if m:
		xxState = m.group(1)
	else:
		print(_sStateTemp)
		xxState = "?"
	xxPPid = int(_pre_map["PPid"])
	_listUIDTemp = re.split("(\s+)", _pre_map["Uid"])
	_listGIDTemp = re.split("(\s+)", _pre_map["Gid"])
	_listUID = [ int(_listUIDTemp[0]), int(_listUIDTemp[2]), int(_listUIDTemp[4]), int(_listUIDTemp[6]) ]	# real, effective, saved, fs
	_listGID = [ int(_listGIDTemp[0]), int(_listGIDTemp[2]), int(_listGIDTemp[4]), int(_listGIDTemp[6]) ]	# real, effective, saved, fs
	xxVMSizeKB = None
	if "VmSize" in _pre_map:
		_vmSizeTemp = re.split("(\s+)", _pre_map["VmSize"])
		assert len(_vmSizeTemp) == 3
		assert _vmSizeTemp[2] == "kB"
		xxVMSizeKB = int(_vmSizeTemp[0])
	xxUID = _listUID[1]
	xxGID = _listGID[1]
	xxUserName = userIDToNameMap.get(xxUID, None) if userIDToNameMap else None
	xxGroupName = grpIDToNameMap.get(xxGID, None) if grpIDToNameMap else None

	#### /proc/????/cmdline ####

	xxCmd = None
	xxArgs = None
	with open(os.path.join(dirPath, "cmdline"), "r") as f:
		_cmdLine = f.read().rstrip("\x00").split("\x00")
		if _cmdLine:
			xxArgs = _cmdLine[1:]
			xxCmd = _cmdLine[0]
	if not xxCmd:
		assert xxProcName
		xxCmd = "[" + xxProcName + "]"

	#### /proc/????/cwd ####

	try:
		# NOTE: if we don't own this we can only read this as root
		xxCWD = os.readlink(os.path.join(dirPath, "cwd"))
	except:
		xxCWD = None

	#### /proc/????/exe ####

	try:
		# NOTE: if we don't own this we can only read this as root
		xxEXE = os.readlink(os.path.join(dirPath, "exe"))
	except:
		xxEXE = None

	# ----------------

	# sometimes xxArgs has not been provided with "\x00" but space as separator; compensate for this though this might not be perfect;
	if xxCmd and xxEXE:
		if xxCmd.startswith(xxEXE + " "):
			xxArgs = xxCmd[len(xxEXE)+1:].strip().split(" ")
			xxCmd = xxEXE

	assert xxCmd is not None
	assert xxArgs is not None

	# ----------------

	ret = {
		"args": " ".join(xxArgs),
		"argsv": xxArgs,
		"cmd": xxCmd,
		"pid": pid,
		"ppid": xxPPid,
		"stat": xxState,
	}
	if xxUserName is not None:
		ret["user"] = xxUserName
	if xxGroupName is not None:
		ret["group"] = xxGroupName
	if xxCWD is not None:
		ret["cwd"] = xxCWD
	if xxEXE is not None:
		ret["exe"] = xxEXE
	ret["vmsizeKB"] = xxVMSizeKB if xxVMSizeKB is not None else -1

	# ----------------

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
def get_ps_local(c = None, bAddVMemSize:bool = False, userIDToNameMap:typing.Dict[int,str] = None, grpIDToNameMap:typing.Dict[int,str] = None) -> typing.List[dict]:
	if c is not None:
		raise Exception("This process analysis requires fast I/O and therefore can only be run locally!")

	if c is None:
		if userIDToNameMap is None:
			userIDToNameMap = {}
			for entry in pwd.getpwall():
				userIDToNameMap[entry.pw_uid] = entry.pw_name
		if grpIDToNameMap is None:
			grpIDToNameMap = {}
			for entry in grp.getgrall():
				grpIDToNameMap[entry.gr_gid] = entry.gr_name

	# ----

	ret = []
	for fe in os.scandir("/proc"):
		if fe.is_dir(follow_symlinks=False) and re.match("^[1-9][0-9]*$", fe.name):
			ret.append(get_process_info_local(int(fe.name), userIDToNameMap, grpIDToNameMap))

	# ----

	return ret
#





