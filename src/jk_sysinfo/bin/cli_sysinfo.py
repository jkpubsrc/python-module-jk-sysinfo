

import os
import typing
import sys
import re

import jk_typing
import jk_argparsing
import jk_logging
import jk_console
import jk_flexdata

import jk_sysinfo
import jk_sysinfo.entity






class CollectedSystemData(object):

	################################################################################################################################
	## Constants
	################################################################################################################################

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self) -> None:
		self.os_release:jk_flexdata.FlexObject = None
		self.bIsRPi:bool = None
		self.data_lsb_release_a:jk_flexdata.FlexObject = None
		self.data_lshw:jk_flexdata.FlexObject = None
		self.data_proccpu_extra:jk_flexdata.FlexObject = None
		self.data_proccpu_extra:jk_flexdata.FlexObject = None
		self.data_mobo:jk_flexdata.FlexObject = None
		self.data_bios:jk_flexdata.FlexObject = None
		self.data_proccpu:jk_flexdata.FlexObject = None
		self.data_cpu:jk_flexdata.FlexObject = None
		self.data_sensors:jk_flexdata.FlexObject = None
		self.data_sysload:jk_flexdata.FlexObject = None
		self.data_mem:jk_flexdata.FlexObject = None
		self.data_lsblk:jk_flexdata.FlexObject = None
		self.data_reboot:jk_flexdata.FlexObject = None
		self.data_mounts:jk_flexdata.FlexObject = None
		self.data_df:jk_flexdata.FlexObject = None
		self.data_net_info:jk_flexdata.FlexObject = None
		self.data_uptime:jk_flexdata.FlexObject = None
		self.data_df:jk_flexdata.FlexObject = None

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

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

#






class CLISysInfo(object):

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

	def __createArgsParser(self) -> jk_argparsing.ArgsParser:
		ap = jk_argparsing.ArgsParser(os.path.basename(__file__), "Display system information in a human readable way.")

		ap.optionDataDefaults.set("help", False)
		ap.optionDataDefaults.set("color", True)

		ap.createOption('h', 'help', "Display this help text.").onOption = \
			lambda argOption, argOptionArguments, parsedArgs: \
				parsedArgs.optionData.set("help", True)
		ap.createOption(None, 'color', "Force using colors in output.").onOption = \
			lambda argOption, argOptionArguments, parsedArgs: \
				parsedArgs.optionData.set("color", False)
		ap.createOption(None, 'no-color', "Don't use colors in output.").onOption = \
			lambda argOption, argOptionArguments, parsedArgs: \
				parsedArgs.optionData.set("color", False)

		ap.createAuthor("Jürgen Knauth", "jk@binary-overflow.de")
		ap.setLicense("Apache", YEAR = "2021-2024", COPYRIGHTHOLDER = "Jürgen Knauth")

		ap.createReturnCode(0, "Everything is okay.")
		ap.createReturnCode(1, "An error occurred.")

		return ap
	#

	def __printFlags(self, text:str, flags:typing.Iterable[str]):
		_t = []
		for _c in text:
			if _c == "\t":
				_t.append(_c)
			else:
				_t.append(' ')
		textEmpty = "".join(_t)

		print(text, end="")

		i = 0
		for flag in flags:
			if i == 20:
				# line break
				print(",")
				print(textEmpty, end="")
				i = 0
			else:
				if i > 0:
					# add comma
					print(", ", end="")
				i += 1
			print(flag, end="")
		print()
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# Collect all data and return it.
	#
	# @param	fabric.Connection c			(optional) A fabric connection object.
	# @return	CollectedSystemData			(always) The collected system data.
	#
	def collectSystemData(self, c = None) -> CollectedSystemData:
		#collectedSystemData = CollectedSystemData()
		ret = CollectedSystemData()

		ret.os_release = jk_flexdata.createFromData(jk_sysinfo.get_etc_os_release(c))

		ret.bIsRPi = ret.os_release.distribution == "raspbian"

		ret.data_lsb_release_a = jk_flexdata.createFromData(jk_sysinfo.get_lsb_release_a(c))				# static
		ret.data_lshw = jk_flexdata.createFromData(jk_sysinfo.get_lshw(c))									# static
		if ret.bIsRPi:
			ret.data_proccpu_extra = jk_flexdata.createFromData(jk_sysinfo.get_proc_cpu_info(c)[1])			# static
			_data_mobo_json = {
				"vendor": "Raspberry Pi Foundation",
			}
			if ret.data_proccpu_extra.hardware:
				_data_mobo_json["soc"] = ret.data_proccpu_extra.hardware
				_data_mobo_json["serial"] = ret.data_proccpu_extra.serial
				_data_mobo_json["name"] = ret.data_proccpu_extra.model
			ret.data_mobo = jk_flexdata.createFromData(_data_mobo_json)
		else:
			ret.data_mobo = jk_flexdata.createFromData(jk_sysinfo.get_motherboard_info(c))					# static
		ret.data_bios = jk_flexdata.createFromData(jk_sysinfo.get_bios_info(c))								# static
		ret.data_proccpu = [ jk_flexdata.createFromData(x) for x in jk_sysinfo.get_proc_cpu_info(c)[0] ]	# static, (runtime)
		ret.data_cpu = jk_flexdata.createFromData(jk_sysinfo.get_cpu_info(c))								# static
		if ret.bIsRPi:
			_t = jk_sysinfo.get_vcgencmd_measure_temp(c)
			_v = jk_sysinfo.get_vcgencmd_measure_volts(c)
			_data_sensors_json = {
				"coretemp": {
					"device": "coretemp",
					"sensorData": {
						"temp1": {
							"sensor": "temp",
							"value": _t["cpu"]["temp"],
						}
					}
				},
				"corevolts": {
					"device": "corevolts",
					"sensorData": {
						"temp1": {
							"sensor": "volt",
							"value": _v["cpu"]["volt"],
						}
					}
				},
				"ramolts": {
					"device": "ramvolts",
					"sensorData": {
						"volt1": {
							"sensor": "volt",
							"value": _v["ram"]["volt"],
						}
					}
				}
			}
			ret.data_sensors = jk_flexdata.createFromData(_data_sensors_json)								# runtime
		else:
			ret.data_sensors = jk_flexdata.createFromData(jk_sysinfo.get_sensors(c))						# runtime
		ret.data_sysload = jk_flexdata.createFromData(jk_sysinfo.get_proc_load_avg(c))						# runtime
		ret.data_mem = jk_flexdata.createFromData(jk_sysinfo.get_proc_meminfo(c))							# runtime
		ret.data_lsblk = jk_flexdata.createFromData(jk_sysinfo.get_lsblk(c))								# runtime
		ret.data_reboot = jk_flexdata.createFromData(jk_sysinfo.get_needs_reboot(c))						# runtime
		ret.data_mounts = jk_flexdata.createFromData(jk_sysinfo.get_mount(c))								# runtime
		ret.data_df = jk_flexdata.createFromData(jk_sysinfo.get_df(c))										# runtime
		ret.data_net_info = jk_flexdata.createFromData(jk_sysinfo.get_net_info(c))							# runtime
		ret.data_uptime = jk_flexdata.createFromData(jk_sysinfo.get_uptime(c))								# runtime

		if not ret.data_reboot:
			print(jk_console.Console.ForeGround.RED + "WARNING: Packet 'needrestart' not installed." + jk_console.Console.RESET)

		return ret
	#

	def printCollectedSystemData(self, csd:CollectedSystemData) -> None:
		assert isinstance(csd, CollectedSystemData)

		################################################################

		print("\n#### bios ####\n")
		print("static")
		print("\tvendor:", csd.data_bios.vendor)
		print("\tversion:", csd.data_bios.version)
		print("\tdate:", csd.data_bios.date)
		print("-")

		################################################################

		print("\n#### motherboard ####\n")
		print("static")
		print("\tvendor:", csd.data_mobo.vendor)
		print("\tname:", csd.data_mobo.name)
		print("\tversion:", csd.data_mobo.version)
		print("-")

		################################################################

		print("\n#### busses and bus devices ####\n")
		print("static")

		def _printPCIStruct(data:jk_flexdata.FlexObject, indent:str=""):
			print(indent + data["class"].upper()
				+ " " + (data.product if data.product else "-")
				+ " (" + data.vendor + ")"
				+ " " + (data.description if data.description else "-")
			)
			if data.children:
				for c in data.children:
					_printPCIStruct(c, indent=indent + "\t")
		#

		_bridge = csd.data_lshw._findR(_class="bridge")
		_printPCIStruct(_bridge, indent="\t")
		print("-")

		################################################################

		print("\n#### system ####\n")
		print("static")
		print("\thostname:", csd.data_lshw.id)	# hostname
		print("\tos distribution:", csd.data_lsb_release_a.distribution)
		print("\tos version:", csd.data_lsb_release_a.version)
		print("\tis LTS version:", csd.data_lsb_release_a.lts)
		print("runtime")
		print("\tprocesses:", csd.data_sysload.processes_total)
		print("\tsystem load:", csd.data_sysload.load1, "/", csd.data_sysload.load5, "/", csd.data_sysload.load15)
		days, hours, minutes, seconds, milliseconds = jk_sysinfo.convertSecondsToHumanReadableDuration(csd.data_uptime.uptimeInSeconds)
		print("\tuptime:", days, "day(s),", hours, "hour(s),", minutes, "minute(s),", seconds, "second(s)")
		if csd.data_reboot.needsReboot:
			updatesRequired = set()
			if csd.data_reboot.updateMicroCodeOrABI:
				updatesRequired.add("CPU or ABI")
			if csd.data_reboot.updateKernel:
				updatesRequired.add("kernel")
			if not updatesRequired:
				raise Exception()
			print(jk_console.Console.ForeGround.ORANGE + "\tUpdate required:", ",".join(updatesRequired) + jk_console.Console.RESET)
		print("-")

		################################################################

		print("\n#### cpu ####\n")
		print("static")
		print("\tvendor:", csd.data_proccpu[0].vendor_id)
		print("\tmodel:", csd.data_proccpu[0].model_name)
		print("\tspeed:", jk_sysinfo.formatFrequencyRangeS(csd.data_cpu.freq_min * 1000000, csd.data_cpu.freq_max * 1000000))
		print("\tcpu family:", csd.data_proccpu[0].cpu_family)
		print("\tcores:", len(csd.data_proccpu), "(hyperthreading)" if ("ht" in csd.data_proccpu[0].flags) else "(no hyperthreading)")
		if "cache_size" in csd.data_proccpu[0]._keys():
			print("\tcpu cache size:", csd.data_proccpu[0].cache_size)
		if csd.data_proccpu[0].flags:
			self.__printFlags("\tflags: ", csd.data_proccpu[0].flags)
		if csd.data_proccpu[0].bugs:
			self.__printFlags("\tbugs: ", csd.data_proccpu[0].bugs)

		bHyperThreading = ("ht" in csd.data_proccpu[0].flags)
		print("\thas hyperthreading:", "yes" if bHyperThreading else "no")

		bHardwareVirtualization = ("vmx" in csd.data_proccpu[0].flags) or ("svm" in csd.data_proccpu[0].flags)
		print("\thas hardware virtualization:", "yes" if bHardwareVirtualization else "no")

		bCryptography = ("aes" in csd.data_proccpu[0].flags) or ("ace" in csd.data_proccpu[0].flags) or ("ace2" in csd.data_proccpu[0].flags)
		print("\thas hardware cryptography:", "yes" if bCryptography else "no")

		print("-")

		################################################################

		print("\n#### memory ####\n")
		print("runtime")
		_mem = csd.data_lshw._findR(id="memory")
		assert _mem.units == "bytes"
		#print("size:", jk_sysinfo.formatBytesS(int(mem.size)))
		print("\tmem total:", jk_sysinfo.formatBytesS(csd.data_mem.MemTotal * 1024))
		print("\tmem available:", jk_sysinfo.formatBytesS(csd.data_mem.MemAvailable * 1024))
		print("\tmem free:", jk_sysinfo.formatBytesS(csd.data_mem.MemFree * 1024))
		print("\tmem buffers:", jk_sysinfo.formatBytesS(csd.data_mem.Buffers * 1024))
		print("\tmem cached:", jk_sysinfo.formatBytesS(csd.data_mem.Cached * 1024))
		print("\tswap total:", jk_sysinfo.formatBytesS(csd.data_mem.SwapTotal * 1024))
		print("\tswap free:", jk_sysinfo.formatBytesS(csd.data_mem.SwapFree * 1024))
		print("\tswap cached:", jk_sysinfo.formatBytesS(csd.data_mem.SwapCached * 1024))
		print("-")

		################################################################

		print("\n#### display ####\n")
		print("static")
		for _display in csd.data_lshw._findAllR(id="display"):
			print("\tvendor:", _display.vendor)
			print("\tproduct:", _display.product)
			print("\tdriver:", _display.configuration.driver)
			print("-")

		################################################################

		print("\n#### storage ####\n")
		print("static")
		#for storage in data_lshw._findAllR(id="storage"):
		#	print("\tvendor:", storage.vendor)
		#	print("\tproduct:", storage.product)
		#	print("\tdescription:", storage.description)
		#	print("\tdriver:", storage.configuration.driver)
		#	print("-")
		#for storage in data_lshw._findAllR(id="cdrom"):
		#	print("\tvendor:", storage.vendor)
		#	print("\tproduct:", storage.product)
		#	print("\tdescription:", storage.description)
		#	print("-")

		_data_lsblk_disks = jk_sysinfo.filter_lsblk_devtree(csd.data_lsblk._toDict(), type="disk")
		_diskTable = jk_console.SimpleTable()
		_diskTable.addRow(
			"device",
			"model",
			"vendor",
			"serial",
			"firmwareRevision",
			"formFactor",
			"diskGranularity",
			"rotationRate",
			"transport",
			"size",
			"uuid",
			"readOnly",
			"rotational",
			"hotplug",
			"NCQ",
			"TRIM",
		).hlineAfterRow = True
		for _jDisk in _data_lsblk_disks:
			_devicePath = _jDisk["dev"]
			_data_hdparam_I = jk_sysinfo.get_hdparm_I(devPath=_devicePath)
			_di = jk_sysinfo.entity.DriveInfo(_jDisk, _data_hdparam_I)
			_diskTable.addRow(
				_di.devicePath,
				_di.model,
				_di.vendor,
				_di.serial,
				_di.firmwareRevision,
				_di.formFactor,
				_di.diskGranularity,
				_di.nominalMediaRotationRate,
				_di.transport,
				_di.size,
				_di.uuid if _di.uuid else "-",
				_di.isReadOnly,
				_di.isRotational,
				_di.isHotplug,
				_di.isNCQSupported,
				_di.isTRIMSupported,
			)	
		_diskTable.print(prefix="\t")
		print("-")

		################################################################

		print("\n#### multimedia ####\n")
		print("static")
		for _multimedia in csd.data_lshw._findAllR(id="multimedia"):
			print("\tvendor:", _multimedia.vendor)
			print("\tproduct:", _multimedia.product)
			print("\tdriver:", _multimedia.configuration.driver)
			print("-")

		################################################################

		print("\n#### network (hardware) ####\n")
		print("static")
		for _network in list(csd.data_lshw._findAllR(id="network")) + list(csd.data_lshw._findAllR(id=re.compile("^network:"))):
			# import jk_json
			# jk_json.prettyPrint(_network._toDict())
			print("\tvendor:", _network.vendor)
			print("\tproduct:", _network.product)
			print("\tdevice:", _network.logicalname)		# network device name
			if _network.configuration.link:
				print("\thas_link:", _network.configuration.link == "yes")
			else:
				print("\thas_link:", "unknown")
			if _network.capabilities.tp or _network.capabilities.ethernet:
				# regular twisted pair network

				if _network.maxSpeedInBitsPerSecond:
					speed, unit = jk_sysinfo.formatBitsPerSecond(_network.maxSpeedInBitsPerSecond)
					print("\tspeed maximum:", speed, unit)					# general speed in bits/s

				if _network.configuration.speed:
					print("\tspeed current:", _network.configuration.speed)			# current speed
				if _network.configuration.duplex:
					print("\tduplex:", _network.configuration.duplex)

			elif _network.configuration.wireless:
				# regular wireless network

				print("\twireless standard:", _network.configuration.wireless)			# "IEEE 802.11"

			else:
				raise Exception("Unknown network type")

			print("\tdescription:", _network.description)
			print("\tdriver:", _network.configuration.driver)
			print("\tmac_addr:", _network.serial)
			print("-")

		################################################################

		print("\n#### sensors ####\n")

		def _formatSensorData(data:jk_flexdata.FlexObject) -> typing.Tuple[str,str,str]:
			if data._isEmpty():
				return "n/a"
			if data.sensor == "volt":
				return str(data.value) + "V"
			if data.sensor == "fan":
				return str(data.value) + " rpm"
			elif data.sensor == "temp":
				_bar, _text = jk_sysinfo.formatTemperatureGraphC2(data.value, data.crit if data.crit else 100)
				if data.crit and data.max:
					_extraText = "max: " + str(data.max) + ", crit: " + str(data.crit) + ""
				else:
					_extraText = "n/a"
				return (_bar, _text, _extraText)
			else:
				raise Exception("Unknown: " + repr(data.sensor))
		#

		print("runtime")
		_table = jk_console.SimpleTable()
		_table.addRow(
			"identifier",
			"visualization",
			"data value",
			"range",
		).hlineAfterRow = True
		for _data in csd.data_sensors._values():
			#jk_json.prettyPrint(data._toDict())
			for sensorItemName, sensorItemStruct in _data.sensorData._items():
				_bar, _text, _extraText = _formatSensorData(sensorItemStruct)
				_table.addRow(
					_data.device + "." + sensorItemName,
					_bar,
					_text,
					_extraText,
				)
		_table.print(prefix="\t")
		print("-")

		################################################################

		print("\n#### network (os) ####\n")
		print("runtime")
		_table = jk_console.SimpleTable()
		_table.addRow(
			"ifname",
			"loop",
			"wlan",
			"mac",
			"mtu",
			"rx pkgs",
			"rx dropped",
			"rx errors",
			"tx pkgs",
			"tx dropped",
			"tx errors",
		).hlineAfterRow = True
		for _networkInterface, _networkInterfaceData in csd.data_net_info._items():
			_table.addRow(
				_networkInterface,
				_networkInterfaceData.is_loop,
				_networkInterfaceData.is_wlan,
				_networkInterfaceData.mac_addr,
				_networkInterfaceData.mtu,
				_networkInterfaceData.rx_packets,
				_networkInterfaceData.rx_dropped,
				_networkInterfaceData.rx_errors,
				_networkInterfaceData.tx_packets,
				_networkInterfaceData.tx_dropped,
				_networkInterfaceData.tx_errors,
			)
		_table.print(prefix="\t")
		print("-")

		################################################################

		print("\n#### drives ####\n")

		print("runtime")

		@jk_typing.checkFunctionSignature()
		def _printDevice(data_lsblk:jk_flexdata.FlexObject, data_mounts:jk_flexdata.FlexObject, data_df:jk_flexdata.FlexObject, indent:str=""):
			if data_lsblk.mountpoint and data_lsblk.mountpoint.startswith("/snap"):
				return
			s = indent + data_lsblk.dev

			if data_lsblk.mountpoint:
				s += " @ "
				s += data_lsblk.mountpoint
				sAdd = " :: "
			else:
				sAdd = " :: "

			if data_lsblk.uuid:
				s += sAdd + repr(data_lsblk.uuid)
				sAdd = " ~ "
			if data_lsblk.fstype:
				s += sAdd + data_lsblk.fstype
				sAdd = " ~ "

			print(s)
			indent += "\t"

			if data_mounts and data_lsblk.mountpoint:
				data_df_2 = data_df._get(data_lsblk.mountpoint)
				#jk_json.prettyPrint(data_mounts._toDict())
				#jk_json.prettyPrint(data_df._toDict())
				if data_df_2:
					print(indent
						+ "total:", jk_sysinfo.formatBytesS(data_df_2.spaceTotal)
						+ ", used:", jk_sysinfo.formatBytesS(data_df_2.spaceUsed)
						+ ", free:", jk_sysinfo.formatBytesS(data_df_2.spaceFree)
						+ ", filled:", jk_sysinfo.formatPercentGraphC(data_df_2.spaceUsed, data_df_2.spaceTotal), jk_sysinfo.formatPercent(data_df_2.spaceUsed, data_df_2.spaceTotal)
						)
					#jk_json.prettyPrint(data_df_2._toDict())
				else:
					print(indent + "Not found: " + data_lsblk.mountpoint)

			if data_lsblk.children:
				for c in data_lsblk.children:
					_printDevice(c, data_mounts, data_df, indent)
		#

		# TODO: drive models

		#print(data_lsblk._keys())
		for _d in csd.data_lsblk.deviceTree:
			_printDevice(_d, csd.data_mounts, csd.data_df, "\t")
			# TODO: list logical drives
		print("-")

		################################################################

		print()

	#

	def main(self) -> int:
		ap = self.__createArgsParser()
		parsedArgs = ap.parse()
		#parsedArgs.dump()

		if parsedArgs.optionData["help"]:
			ap.showHelp()
			return 0

		with jk_logging.wrapMain(bColor=parsedArgs.optionData["color"]) as log:
			# if not parsedArgs.optionData["color"]:
			# 	log = jk_logging.ConsoleLogger.create(logMsgFormatter = jk_logging.DEFAULT_LOG_MESSAGE_FORMATTER, printToStdErr = True)

			# ----

			csd = self.collectSystemData()
			self.printCollectedSystemData(csd)
	#

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

#




"""
from fabric import Connection
import jk_pwdinput

REMOTE_HOST = "<ipaddress>"
REMOTE_PORT = 22
REMOTE_LOGIN = "<login>"
REMOTE_PASSWORD = jk_pwdinput.readpwd("Password for " + REMOTE_LOGIN + "@" + REMOTE_HOST + ": ")
c = Connection(host=REMOTE_HOST, user=REMOTE_LOGIN, port=REMOTE_PORT, connect_kwargs={"password": REMOTE_PASSWORD})
"""
c = None









def main():
	app = CLISysInfo()
	sys.exit(app.main())
#













