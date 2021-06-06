

from jk_cachefunccalls import cacheCalls

from jk_cmdoutputparsinghelper import LineList, Table, ColumnDef

from .parsing_utils import *
from .invoke_utils import run




def _parseMark(s:str) -> bool:
	return bool(s)
#




#
# Returns something like this:
#
#	{
#		"automounts": {
#			"proc-sys-fs-binfmt_misc": [
#				false,
#				"proc-sys-fs-binfmt_misc.automount",
#				"loaded",
#				"active",
#				"running",
#				"Arbitrary Executable File Formats File System Automount Point"
#			]
#			....
#		},
#		"devices": {
#			"dev-cdrom": [
#				false,
#				"dev-cdrom.device",
#				"loaded",
#				"active",
#				"plugged",
#				"TSSTcorp_CDDVDW_SH-S203P Gal_Civ_2_DE"
#			],
#			....
#		},
#		"mounts": {
#			"-": [
#				false,
#				"-.mount",
#				"loaded",
#				"active",
#				"mounted",
#				"/"
#			],
#			....
#			"mounts-ramdisk": [
#				false,
#				"mounts-ramdisk.mount",
#				"loaded",
#				"active",
#				"mounted",
#				"/mounts/ramdisk"
#			],
#			....
#		},
#		"paths": {
#			"acpid": [
#				false,
#				"acpid.path",
#				"loaded",
#				"active",
#				"running",
#				"ACPI Events Check"
#			],
#			....
#		},
#		"scopes": {
#			"init": [
#				false,
#				"init.scope",
#				"loaded",
#				"active",
#				"running",
#				"System and Service Manager"
#			],
#			"session-c2": [
#				false,
#				"session-c2.scope",
#				"loaded",
#				"active",
#				"running",
#				"Session c2 of user woodoo"
#			]
#			....
#		},
#		"services": {
#			"accounts-daemon": [
#				false,
#				"accounts-daemon.service",
#				"loaded",
#				"active",
#				"running",
#				"Accounts Service"
#			],
#			....
#			"colord": [
#				false,
#				"colord.service",
#				"loaded",
#				"active",
#				"running",
#				"Manage, Install and Generate Color Profiles"
#			],
#			....
#			"whoopsie": [
#				false,
#				"whoopsie.service",
#				"loaded",
#				"active",
#				"running",
#				"crash report submission daemon"
#			]
#		},
#		"slices": {
#			....
#		},
#		"sockets": {
#			"acpid": [
#				false,
#				"acpid.socket",
#				"loaded",
#				"active",
#				"running",
#				"ACPID Listen Socket"
#			],
#			....
#			"cups": [
#				false,
#				"cups.socket",
#				"loaded",
#				"active",
#				"running",
#				"CUPS Scheduler"
#			],
#			....
#		},
#		"targets": {
#			"basic": [
#				false,
#				"basic.target",
#				"loaded",
#				"active",
#				"active",
#				"Basic System"
#			],
#			....
#			"graphical": [
#				false,
#				"graphical.target",
#				"loaded",
#				"active",
#				"active",
#				"Graphical Interface"
#			],
#			....
#		},
#		"timers": {
#			"apt-daily": [
#				false,
#				"apt-daily.timer",
#				"loaded",
#				"active",
#				"waiting",
#				"Daily apt download activities"
#			],
#			....
#			"motd-news": [
#				false,
#				"motd-news.timer",
#				"loaded",
#				"active",
#				"waiting",
#				"Message of the Day"
#			],
#			....
#		}
#	}
#
def parse_systemctl_units(stdout:str, stderr:str, exitcode:int) -> dict:

	"""
	  UNIT                                                                                     LOAD      ACTIVE   SUB       DESCRIPTION
	  mono-xsp4.service                                                                        loaded    active   running   LSB: Mono XSP4
	  motd-news.service                                                                        loaded    inactive dead      Message of the Day
	● mountkernfs.service                                                                      masked    inactive dead      mountkernfs.service
	  systemd-machine-id-commit.service                                                        loaded    inactive dead      Commit a transient machine-id on disk
	● systemd-modules-load.service                                                             loaded    failed   failed    Load Kernel Modules
	  systemd-networkd-resolvconf-update.service                                               loaded    inactive dead      Update resolvconf for networkd DNS
	  sysinit.target                                                                           loaded    active   active    System Initialization
	● syslog.target                                                                            not-found inactive dead      syslog.target
	  time-sync.target                                                                         loaded    active   active    System Time Synchronized

	LOAD   = Reflects whether the unit definition was properly loaded.
	ACTIVE = The high-level unit activation state, i.e. generalization of SUB.
	SUB    = The low-level unit activation state, values depend on unit type.

	354 loaded units listed.
	To show all installed unit files use 'systemctl list-unit-files'.
	"""

	if exitcode != 0:
		raise Exception()

	# split into list of lines
	lines = LineList(stdout)
	assert isinstance(lines, LineList)

	# now we must separate a trailing description.
	lineNumbers = lines.getLineNumbersOfEmptyLines()
	assert lineNumbers
	assert lineNumbers[0] > 0
	del lines[lineNumbers[0]:]

	# get column split positions
	wordPos = [ 0 ] + getPositionsOfWords(lines[0])
	table = lines.createDataTableFromColumns(wordPos, bLStrip=True, bRStrip=True, bFirstLineIsHeader=True, columnDefs=[
		ColumnDef("MARK", _parseMark),
		ColumnDef("UNIT"),
		ColumnDef("LOAD"),
		ColumnDef("ACTIVE"),
		ColumnDef("SUB"),
		ColumnDef("DESCRIPTION"),
	])

	# build output matrix: use service names as keys
	ret = {}
	for record in table:
		key = record[1]
		pos = key.rfind(".")
		category = key[pos+1:] + "s"			# pluralize the category
		key = key[:pos]

		if category not in ret:
			ret[category] = {}

		ret[category][key] = record

	return ret
#



def get_systemctl_units(c = None) -> dict:
	stdout, stderr, exitcode = run(c, "/bin/systemctl -a list-units")
	return parse_systemctl_units(stdout, stderr, exitcode)
#


















