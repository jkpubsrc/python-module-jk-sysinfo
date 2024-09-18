

import os
import sys
import fabric

import jk_logging
import jk_sysinfo
import jk_json
import jk_argparsing
import jk_typing

from ..cli.ServerCfg import ServerCfg






class ElementarSysInfo(object):

	################################################################################################################################
	## Constants
	################################################################################################################################

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# @param		str argLongOption			The arguments long option
	# @param		str argDescription			The arguments description
	# @param		callable function			The function to that will perform the data retrieval
	# @param		** extraArgs				Extra arguments to pass to the function as arguments
	#
	def __init__(self, argLongOption:str, argDescription:str, function, **kwargs):
		self.longOption = argLongOption
		self.description = argDescription
		self.function = function
		self.extraArgs = kwargs
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

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

	#
	# Perform data retrieval and return the result.
	#
	# @return		list|dict		The result data will be a JSON list or object.
	#
	def run(self, c):
		return self.function(c, **self.extraArgs)
	#

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

#









ALL_SYSINFO_OPTIONS = [
	ElementarSysInfo("i-accesspoints", "Get data about access points", jk_sysinfo.get_accesspoints),
	ElementarSysInfo("i-apt-list-upgradable", "Get information about upgradable packages", jk_sysinfo.get_apt_list_upgradable),
	ElementarSysInfo("i-bios-info", "Get information about the BIOS", jk_sysinfo.get_bios_info),
	ElementarSysInfo("i-cpu-info", "Get information about the CPU", jk_sysinfo.get_cpu_info),
	ElementarSysInfo("i-date", "Get date (local)", jk_sysinfo.get_date, utc=False),
	ElementarSysInfo("i-date-utc", "Get date (UTC)", jk_sysinfo.get_date, utc=True),
	ElementarSysInfo("i-df", "Get disk space information", jk_sysinfo.get_df),
	ElementarSysInfo("i-docker-stats", "Retrieve information about running docker services", jk_sysinfo.get_docker_stats),
	ElementarSysInfo("i-dpkg-list", "Get information about installed packages", jk_sysinfo.get_dpkg_list),
	ElementarSysInfo("i-etc-hostname", "Get hostname information", jk_sysinfo.get_etc_hostname),
	ElementarSysInfo("i-etc-os-release", "Get information about the OS as stored in /etc/os/release", jk_sysinfo.get_etc_os_release),
	ElementarSysInfo("i-ifconfig", "Get information about the network interfaces as provided by 'ifconfig'", jk_sysinfo.get_ifconfig),
	ElementarSysInfo("i-lsb-release-a", "Get information about the current linux distribution", jk_sysinfo.get_lsb_release_a),
	ElementarSysInfo("i-lsblk", "Get information about block devices", jk_sysinfo.get_lsblk),
	ElementarSysInfo("i-lshw", "Get information about the hardware as provided by 'lshw'", jk_sysinfo.get_lshw),
	ElementarSysInfo("i-motherboard-info", "Get information about the motherboard", jk_sysinfo.get_motherboard_info),
	ElementarSysInfo("i-mount", "Get information about the mounted devices", jk_sysinfo.get_mount),
	ElementarSysInfo("i-needs-reboot", "Check if a reboot is required", jk_sysinfo.get_needs_reboot),
	ElementarSysInfo("i-net-info", "Retrieve various information about network devices", jk_sysinfo.get_net_info),
	ElementarSysInfo("i-pip3-list", "Retrieve a list of installed python packages", jk_sysinfo.get_pip3_list),
	ElementarSysInfo("i-proc-cpu-info", "Retrieve information about the CPU as provided by /proc/cpuinfo", jk_sysinfo.get_proc_cpu_info),
	ElementarSysInfo("i-proc-load-avg", "Retrieve information about the system load as provided by /proc/loadavg", jk_sysinfo.get_proc_load_avg),
	ElementarSysInfo("i-proc-meminfo", "Retrieve information about the memory usage as provided by /proc/meminfo", jk_sysinfo.get_proc_meminfo),
	ElementarSysInfo("i-ps", "Get information about processes", jk_sysinfo.get_ps),
	ElementarSysInfo("i-sensors", "Get information about processes", jk_sysinfo.get_sensors),
	ElementarSysInfo("i-systemctl-units", "Get information about all systemctrl units", jk_sysinfo.get_systemctl_units),
	ElementarSysInfo("i-uptime", "Get information about uptime", jk_sysinfo.get_uptime),
	ElementarSysInfo("i-user-info", "Get information about users", jk_sysinfo.get_user_info),
	ElementarSysInfo("i-vcgencmd", "Get information about a Raspberry Pi", jk_sysinfo.get_vcgencmd),
]
if os.getuid() == 0:
	ALL_SYSINFO_OPTIONS.extend([
		ElementarSysInfo("i-etc-group", "Get all data from /etc/group and /etc/gshadow", jk_sysinfo.get_etc_group),
		ElementarSysInfo("i-etc-passwd", "Get all data from /etc/passwd and /etc/shadow", jk_sysinfo.get_etc_passwd),
	])

ALL_SYSINFO_OPTIONS_MAP = {
	opt.longOption:opt for opt in ALL_SYSINFO_OPTIONS
}




class CLISysInfoJSON(object):

	################################################################################################################################
	## Constants
	################################################################################################################################

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self):
		pass
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _onOptionAllAutoDetect(self, argOption, argOptionArguments, parsedArgs):
		for opt in ALL_SYSINFO_OPTIONS:
			if (opt.longOption == "i-vcgencmd") and not jk_sysinfo.has_local_vcgencmd():
				continue
			if (opt.longOption == "i-sensors") and not jk_sysinfo.has_local_sensors():
				continue
			if (opt.longOption == "i-docker-stats") and not jk_sysinfo.has_local_docker():
				continue
			parsedArgs.optionData.set(opt.longOption, True)
	#

	def _onOptionAllStd(self, argOption, argOptionArguments, parsedArgs):
		for opt in ALL_SYSINFO_OPTIONS:
			if opt.longOption in [ "i-vcgencmd" ]:
				continue
			parsedArgs.optionData.set(opt.longOption, True)
	#

	def _onOptionAllVM(self, argOption, argOptionArguments, parsedArgs):
		for opt in ALL_SYSINFO_OPTIONS:
			if opt.longOption in [ "i-vcgencmd" ]:
				continue
			if opt.longOption in [ "i-sensors" ]:
				continue
			parsedArgs.optionData.set(opt.longOption, True)
	#

	def _onOptionAllRPi(self, argOption, argOptionArguments, parsedArgs):
		for opt in ALL_SYSINFO_OPTIONS:
			if opt.longOption in []:
				continue
			parsedArgs.optionData.set(opt.longOption, True)
	#

	def _createArgsParser(self) -> jk_argparsing.ArgsParser:
		ap = jk_argparsing.ArgsParser(os.path.basename(__file__), "Display system information in JSON format.")

		ap.optionDataDefaults.set("help", False)
		ap.optionDataDefaults.set("color", True)
		ap.optionDataDefaults.set("outDirPath", None)
		ap.optionDataDefaults.set("promptPwdStdin", False)

		ap.createOption('h', 'help', "Display this help text.").onOption = \
			lambda argOption, argOptionArguments, parsedArgs: \
				parsedArgs.optionData.set("help", True)
		ap.createOption(None, 'color', "Force using colors in output.").onOption = \
			lambda argOption, argOptionArguments, parsedArgs: \
				parsedArgs.optionData.set("color", False)
		ap.createOption(None, 'no-color', "Don't use colors in output.").onOption = \
			lambda argOption, argOptionArguments, parsedArgs: \
				parsedArgs.optionData.set("color", False)
		ap.createOption(None, 'output-dir-path', "Write all data to individual JSON files in this directory instead of STDOUT.") \
			.expectDirectory("path", minLength=1, mustExist=True) \
			.onOption = \
				lambda argOption, argOptionArguments, parsedArgs: \
					parsedArgs.optionData.set("outDirPath", argOptionArguments[0])
		ap.createOption(None, 'remote', "The path of the configuration file for a remote host to connect to.") \
			.expectFile("file", toAbsolutePath=True, mustExist=True) \
			.onOption = lambda argOption, argOptionArguments, parsedArgs: \
				parsedArgs.optionData.set("remote", argOptionArguments[0])
		ap.createOption(None, 'prompt-pwd-stdin', "If connecting to a remote host prompt for password via STDIN.").onOption = \
			lambda argOption, argOptionArguments, parsedArgs: \
				parsedArgs.optionData.set("promptPwdStdin", True)
		for opt in ALL_SYSINFO_OPTIONS:
			opt.register(ap)

		ap.createOption(None, 'i-all', "Use all system information modules (with autodetect).").onOption = self._onOptionAllAutoDetect
		ap.createOption(None, 'i-all-std', "Use all system information modules (Regular *nix Machines).").onOption = self._onOptionAllStd
		ap.createOption(None, 'i-all-rpi', "Use all system information modules (Raspberry Pi).").onOption = self._onOptionAllRPi
		ap.createOption(None, 'i-all-vm', "Use all system information modules (Virtual Machines).").onOption = self._onOptionAllVM

		ap.createAuthor("Jürgen Knauth", "jk@binary-overflow.de")
		ap.setLicense("Apache", YEAR = "2021-2023", COPYRIGHTHOLDER = "Jürgen Knauth")

		ap.createReturnCode(0, "Everything is okay.")
		ap.createReturnCode(1, "An error occurred.")

		return ap
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def main(self) -> int:
		ap = self._createArgsParser()

		# TODO: create logger with color autodetect here, as parsing might fail here and we should already have good log messages here
		parsedArgs = ap.parse()
		#parsedArgs.dump()

		if parsedArgs.optionData["help"]:
			ap.showHelp()
			return 0

		with jk_logging.wrapMain(bColor=parsedArgs.optionData["color"]) as log:
			#if not parsedArgs.optionData["color"]:
			#	log = jk_logging.ConsoleLogger.create(logMsgFormatter = jk_logging.DEFAULT_LOG_MESSAGE_FORMATTER, printToStdErr = True)

			"""
			cmdName, cmdArgs = parsedArgs.parseNextCommand()
			if cmdName is None:
				ap.showHelp()
				sys.exit(0)
			"""

			# ----

			c = None
			if "remote" in parsedArgs.optionData:
				_serverCfgFilePath = parsedArgs.optionData["remote"]
				serverCfg = ServerCfg.loadFromFile(_serverCfgFilePath)
				if serverCfg.shouldConnectViaUserNamePwd:
					if parsedArgs.optionData.get("promptPwdStdin"):
						serverCfg.readPwdFromSTDINIfPwdMissing()
					if serverCfg.pwd:
						log.notice("Connecting via username and password to " + serverCfg.host + " ...")
						c = fabric.Connection(host=serverCfg.host, user=serverCfg.user, port=serverCfg.port, connect_kwargs={"password": serverCfg.pwd})
					else:
						log.notice("Connecting via username to " + serverCfg.host + " ...")
						c = fabric.Connection(host=serverCfg.host, user=serverCfg.user, port=serverCfg.port)
				elif serverCfg.shouldConnectViaKeyFile:
					_keyFilePath = serverCfg.keyFile
					if not os.path.isabs(_keyFilePath):
						_keyFilePath = os.path.normpath(os.path.join(os.path.dirname(_serverCfgFilePath), _keyFilePath))
					log.notice("Connecting via keyfile to " + serverCfg.host + " ...")
					log.notice("Using key file: " + _keyFilePath)
					c = fabric.Connection(host=serverCfg.host, user=serverCfg.user, port=serverCfg.port, connect_kwargs={"key_filename": _keyFilePath})
				else:
					raise Exception()

			# ----

			bSuccess = True

			ret = {}
			for opt in ALL_SYSINFO_OPTIONS:
				if parsedArgs.optionData[opt.longOption]:
					try:
						ret[opt.longOption] = opt.run(c)
					except Exception as ee:
						# there has been an error
						ret[opt.longOption] = None
						# log.error("Failed to retrieve data for: " + opt.longOption)
						log.exception(ee)
						bSuccess = False

			# ----

			if not ret:
				ap.showHelp()
				return 0

			# ----

			outDirPath = parsedArgs.optionData["outDirPath"]
			if outDirPath:
				for k,v in ret.items():
					filePath = os.path.join(outDirPath, k + ".json")
					jk_json.saveToFilePretty(v, filePath)
			else:
				jk_json.prettyPrint(ret)

			# ----

			return 0 if bSuccess else 1
	#

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

#











def main():
	app = CLISysInfoJSON()
	sys.exit(app.main())
#













