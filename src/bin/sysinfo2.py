#!/usr/bin/python3


import os
import sys
import re

import jk_console
import jk_sysinfo
import jk_json
import jk_flexdata
import jk_logging
from jk_typing import *
import jk_argparsing







class SysInfoOption(object):

	def __init__(self, longOption:str, description:str, function, **kwargs):
		self.longOption = longOption
		self.description = description
		self.function = function
		self.extraArgs = kwargs
	#

	def onOptionEnable(self, argOption, argOptionArguments, parsedArgs):
		parsedArgs.optionData.set(self.longOption, True)
	#

	def onOptionDisable(self, argOption, argOptionArguments, parsedArgs):
		parsedArgs.optionData.set(self.longOption, False)
	#

	def register(self, ap:jk_argparsing.ArgsParser):
		ap.optionDataDefaults.set(self.longOption, False)
		c = ap.createOption(None, self.longOption, self.description + " (enable)").onOption = self.onOptionEnable
		c = ap.createOption(None, self.longOption + "-0", self.description + " (disable)").onOption = self.onOptionDisable
	#

	def run(self, c):
		return self.function(c, **self.extraArgs)
	#

#





ALL_SYSINFO_OPTIONS = [
	SysInfoOption("i-accesspoints", "Get data about access points", jk_sysinfo.get_accesspoints),
	SysInfoOption("i-apt-list-upgradable", "Get information about upgradable packages", jk_sysinfo.get_apt_list_upgradable),
	SysInfoOption("i-bios-info", "Get information about the BIOS", jk_sysinfo.get_bios_info),
	SysInfoOption("i-cpu-info", "Get information about the CPU", jk_sysinfo.get_cpu_info),
	SysInfoOption("i-date", "Get date (local)", jk_sysinfo.get_date, utc=False),
	SysInfoOption("i-date-utc", "Get date (UTC)", jk_sysinfo.get_date, utc=True),
	SysInfoOption("i-df", "Get disk space information", jk_sysinfo.get_df),
	SysInfoOption("i-dpkg-list", "Get information about installed packages", jk_sysinfo.get_dpkg_list),
	SysInfoOption("i-etc-hostname", "Get hostname information", jk_sysinfo.get_etc_hostname),
	SysInfoOption("i-etc-os-release", "Get information about the OS as stored in /etc/os/release", jk_sysinfo.get_etc_os_release),
	SysInfoOption("i-ifconfig", "Get information about the network interfaces as provided by 'ifconfig'", jk_sysinfo.get_ifconfig),
	SysInfoOption("i-lsb-release-a", "Get information about the current linux distribution", jk_sysinfo.get_lsb_release_a),
	SysInfoOption("i-lsblk", "Get information about block devices", jk_sysinfo.get_lsblk),
	SysInfoOption("i-lshw", "Get information about the hardware as provided by 'lshw'", jk_sysinfo.get_lshw),
	SysInfoOption("i-motherboard-info", "Get information about the motherboard", jk_sysinfo.get_motherboard_info),
	SysInfoOption("i-mount", "Get information about the mounted devices", jk_sysinfo.get_mount),
	SysInfoOption("i-needs-reboot", "Check if a reboot is required", jk_sysinfo.get_needs_reboot),
	SysInfoOption("i-net-info", "Retrieve various information about network devices", jk_sysinfo.get_net_info),
	SysInfoOption("i-pip3-list", "Retrieve a list of installed python packages", jk_sysinfo.get_pip3_list),
	SysInfoOption("i-proc-cpu-info", "Retrieve information about the CPU as provided by /proc/cpuinfo", jk_sysinfo.get_proc_cpu_info),
	SysInfoOption("i-proc-load-avg", "Retrieve information about the system load as provided by /proc/loadavg", jk_sysinfo.get_proc_load_avg),
	SysInfoOption("i-proc-meminfo", "Retrieve information about the memory usage as provided by /proc/meminfo", jk_sysinfo.get_proc_meminfo),
	SysInfoOption("i-ps", "Get information about processes", jk_sysinfo.get_ps),
	SysInfoOption("i-sensors", "Get information about processes", jk_sysinfo.get_sensors),
	SysInfoOption("i-uptime", "Get information about uptime", jk_sysinfo.get_uptime),
	SysInfoOption("i-user-info", "Get information about users", jk_sysinfo.get_user_info),
	SysInfoOption("i-vcgencmd", "Get information about a Raspberry Pi", jk_sysinfo.get_vcgencmd),
]
if os.getuid() == 0:
	ALL_SYSINFO_OPTIONS.extend([
		SysInfoOption("i-etc-group", "Get all data from /etc/group and /etc/gshadow", jk_sysinfo.get_etc_group),
		SysInfoOption("i-etc-passwd", "Get all data from /etc/passwd and /etc/shadow", jk_sysinfo.get_etc_passwd),
	])

ALL_SYSINFO_OPTIONS_MAP = {
	opt.longOption:opt for opt in ALL_SYSINFO_OPTIONS
}

def onOptionAll(argOption, argOptionArguments, parsedArgs):
	for opt in ALL_SYSINFO_OPTIONS:
		parsedArgs.optionData.set(opt.longOption, True)
#

def onOptionAllStd(argOption, argOptionArguments, parsedArgs):
	for opt in ALL_SYSINFO_OPTIONS:
		if opt.longOption in [ "i-vcgencmd" ]:
			continue
		parsedArgs.optionData.set(opt.longOption, True)
#

def onOptionAllRPi(argOption, argOptionArguments, parsedArgs):
	for opt in ALL_SYSINFO_OPTIONS:
		if opt.longOption in []:
			continue
		parsedArgs.optionData.set(opt.longOption, True)
#





ap = jk_argparsing.ArgsParser("sysinfo2", "Display system information.")

ap.optionDataDefaults.set("help", False)
ap.optionDataDefaults.set("color", True)

ap.createOption('h', 'help', "Display this help text.").onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("help", True)
ap.createOption(None, 'no-color', "Dont' use colors in output.").onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("colors", False)
for opt in ALL_SYSINFO_OPTIONS:
	opt.register(ap)
ap.createOption(None, 'i-all', "Use all system information modules.").onOption = onOptionAll
ap.createOption(None, 'i-all-std', "Use all system information modules (Standard).").onOption = onOptionAllStd
ap.createOption(None, 'i-all-rpi', "Use all system information modules (Raspberry Pi).").onOption = onOptionAllRPi

ap.createAuthor("Jürgen Knauth", "jk@binary-overflow.de")
ap.setLicense("Apache", YEAR = 2020, COPYRIGHTHOLDER = "Jürgen Knauth")

ap.createReturnCode(0, "Everything is okay.")
ap.createReturnCode(1, "An error occurred.")






parsedArgs = ap.parse()
#parsedArgs.dump()

if parsedArgs.optionData["help"]:
	ap.showHelp()
	sys.exit(0)

"""
cmdName, cmdArgs = parsedArgs.parseNextCommand()
if cmdName is None:
	ap.showHelp()
	sys.exit(0)
"""

if parsedArgs.optionData["color"]:
	log = jk_logging.ConsoleLogger.create(logMsgFormatter = jk_logging.COLOR_LOG_MESSAGE_FORMATTER, printToStdErr = True)
else:
	log = jk_logging.ConsoleLogger.create(printToStdErr = True)

bSuccess = True

ret = {}
for opt in ALL_SYSINFO_OPTIONS:
	if parsedArgs.optionData[opt.longOption]:
		try:
			ret[opt.longOption] = opt.run(None)
		except Exception as ee:
			# there has been an error
			ret[opt.longOption] = None
			# log.error("Failed to retrieve data for: " + opt.longOption)
			log.exception(ee)

jk_json.prettyPrint(ret)

sys.exit(0 if bSuccess else 1)










