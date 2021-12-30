#!/usr/bin/python3


import os
import sys
import re

import jk_console
import jk_json
import jk_flexdata
from jk_typing import *

import jk_sysinfo
import jk_sysinfo.entity










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



x = jk_sysinfo.get_etc_os_release(c)
os_release = jk_flexdata.createFromData(jk_sysinfo.get_etc_os_release(c))

bIsRPi = os_release.distribution == "raspbian"





data_lsb_release_a = jk_flexdata.createFromData(jk_sysinfo.get_lsb_release_a(c))				# static
data_lshw = jk_flexdata.createFromData(jk_sysinfo.get_lshw(c))									# static
if bIsRPi:
	data_proccpu_extra = jk_flexdata.createFromData(jk_sysinfo.get_proc_cpu_info(c)[1])			# static
	data_mobo_json = {
		"vendor": "Raspberry Pi Foundation",
	}
	if data_proccpu_extra.hardware:
		data_mobo_json["soc"] = data_proccpu_extra.hardware
		data_mobo_json["serial"] = data_proccpu_extra.serial
		data_mobo_json["name"] = data_proccpu_extra.model
	data_mobo = jk_flexdata.createFromData(data_mobo_json)
else:
	data_mobo = jk_flexdata.createFromData(jk_sysinfo.get_motherboard_info(c))					# static
data_bios = jk_flexdata.createFromData(jk_sysinfo.get_bios_info(c))								# static
data_proccpu = [ jk_flexdata.createFromData(x) for x in jk_sysinfo.get_proc_cpu_info(c)[0] ]	# static, (runtime)
data_cpu = jk_flexdata.createFromData(jk_sysinfo.get_cpu_info(c))								# static
if bIsRPi:
	t = jk_sysinfo.get_vcgencmd_measure_temp(c)
	v = jk_sysinfo.get_vcgencmd_measure_volts(c)
	data_sensors_json = {
		"coretemp": {
			"device": "coretemp",
			"sensorData": {
				"temp1": {
					"sensor": "temp",
					"value": t["cpu"]["temp"],
				}
			}
		},
		"corevolts": {
			"device": "corevolts",
			"sensorData": {
				"temp1": {
					"sensor": "volt",
					"value": v["cpu"]["volt"],
				}
			}
		},
		"ramolts": {
			"device": "ramvolts",
			"sensorData": {
				"volt1": {
					"sensor": "volt",
					"value": v["ram"]["volt"],
				}
			}
		}
	}
	data_sensors = jk_flexdata.createFromData(data_sensors_json)								# runtime
else:
	data_sensors = jk_flexdata.createFromData(jk_sysinfo.get_sensors(c))						# runtime
data_sysload = jk_flexdata.createFromData(jk_sysinfo.get_proc_load_avg(c))						# runtime
data_mem = jk_flexdata.createFromData(jk_sysinfo.get_proc_meminfo(c))							# runtime
data_lsblk = jk_flexdata.createFromData(jk_sysinfo.get_lsblk(c))								# runtime
data_reboot = jk_flexdata.createFromData(jk_sysinfo.get_needs_reboot(c))						# runtime
data_mounts = jk_flexdata.createFromData(jk_sysinfo.get_mount(c))								# runtime
data_df = jk_flexdata.createFromData(jk_sysinfo.get_df(c))										# runtime
data_net_info = jk_flexdata.createFromData(jk_sysinfo.get_net_info(c))							# runtime
data_uptime = jk_flexdata.createFromData(jk_sysinfo.get_uptime(c))								# runtime

if not data_reboot:
	print(jk_console.Console.ForeGround.RED + "WARNING: Packet 'needrestart' not installed." + jk_console.Console.RESET)






################################################################

print("\n#### bios ####\n")
print("static")
print("\tvendor:", data_bios.vendor)
print("\tversion:", data_bios.version)
print("\tdate:", data_bios.date)
print("-")

################################################################

print("\n#### motherboard ####\n")
print("static")
print("\tvendor:", data_mobo.vendor)
print("\tname:", data_mobo.name)
print("\tversion:", data_mobo.version)
print("-")

################################################################

print("\n#### busses and bus devices ####\n")
print("static")

def printPCIStruct(data:jk_flexdata.FlexObject, indent:str=""):
	print(indent + data["class"].upper()
		+ " " + (data.product if data.product else "-")
		+ " (" + data.vendor + ")"
		+ " " + (data.description if data.description else "-")
	)
	if data.children:
		for c in data.children:
			printPCIStruct(c, indent=indent + "\t")
#

bridge = data_lshw._findR(_class="bridge")
printPCIStruct(bridge, indent="\t")
print("-")

################################################################

print("\n#### system ####\n")
print("static")
print("\thostname:", data_lshw.id)	# hostname
print("\tos distribution:", data_lsb_release_a.distribution)
print("\tos version:", data_lsb_release_a.version)
print("\tis LTS version:", data_lsb_release_a.lts)
print("runtime")
print("\tprocesses:", data_sysload.processes_total)
print("\tsystem load:", data_sysload.load1, "/", data_sysload.load5, "/", data_sysload.load15)
days, hours, minutes, seconds, milliseconds = jk_sysinfo.convertSecondsToHumanReadableDuration(data_uptime.uptimeInSeconds)
print("\tuptime:", days, "day(s),", hours, "hour(s),", minutes, "minute(s),", seconds, "second(s)")
if data_reboot.needsReboot:
	updatesRequired = set()
	if data_reboot.updateMicroCodeOrABI:
		updatesRequired.add("CPU or ABI")
	if data_reboot.updateKernel:
		updatesRequired.add("kernel")
	if not updatesRequired:
		raise Exception()
	print(jk_console.Console.ForeGround.ORANGE + "\tUpdate required:", ",".join(updatesRequired) + jk_console.Console.RESET)
print("-")

################################################################

print("\n#### cpu ####\n")
print("static")
print("\tvendor:", data_proccpu[0].vendor_id)
print("\tmodel:", data_proccpu[0].model_name)
print("\tspeed:", jk_sysinfo.formatFrequencyRangeS(data_cpu.freq_min * 1000000, data_cpu.freq_max * 1000000))
print("\tcpu family:", data_proccpu[0].cpu_family)
print("\tcores:", len(data_proccpu), "(hyperthreading)" if ("ht" in data_proccpu[0].flags) else "")
if "cache_size" in data_proccpu[0]._keys():
	print("\tcpu cache size:", data_proccpu[0].cache_size)
if data_proccpu[0].bugs:
	print("\tbugs:", ", ".join(data_proccpu[0].bugs))
print("-")

################################################################

print("\n#### memory ####\n")
print("runtime")
mem = data_lshw._findR(id="memory")
assert mem.units == "bytes"
#print("size:", jk_sysinfo.formatBytesS(int(mem.size)))
print("\tmem total:", jk_sysinfo.formatBytesS(data_mem.MemTotal * 1024))
print("\tmem available:", jk_sysinfo.formatBytesS(data_mem.MemAvailable * 1024))
print("\tmem free:", jk_sysinfo.formatBytesS(data_mem.MemFree * 1024))
print("\tmem buffers:", jk_sysinfo.formatBytesS(data_mem.Buffers * 1024))
print("\tmem cached:", jk_sysinfo.formatBytesS(data_mem.Cached * 1024))
print("\tswap total:", jk_sysinfo.formatBytesS(data_mem.SwapTotal * 1024))
print("\tswap free:", jk_sysinfo.formatBytesS(data_mem.SwapFree * 1024))
print("\tswap cached:", jk_sysinfo.formatBytesS(data_mem.SwapCached * 1024))
print("-")

################################################################

print("\n#### display ####\n")
print("static")
for display in data_lshw._findAllR(id="display"):
	print("\tvendor:", display.vendor)
	print("\tproduct:", display.product)
	print("\tdriver:", display.configuration.driver)
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

data_lsblk_disks = jk_sysinfo.filter_lsblk_devtree(data_lsblk._toDict(), type="disk")
diskTable = jk_console.SimpleTable()
diskTable.addRow(
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
for jDisk in data_lsblk_disks:
	devicePath = jDisk["dev"]
	data_hdparam_I = jk_sysinfo.get_hdparm_I(devPath=devicePath)
	di = jk_sysinfo.entity.DriveInfo(jDisk, data_hdparam_I)
	diskTable.addRow(
		di.devicePath,
		di.model,
		di.vendor,
		di.serial,
		di.firmwareRevision,
		di.formFactor,
		di.diskGranularity,
		di.nominalMediaRotationRate,
		di.transport,
		di.size,
		di.uuid if di.uuid else "-",
		di.isReadOnly,
		di.isRotational,
		di.isHotplug,
		di.isNCQSupported,
		di.isTRIMSupported,
	)	
diskTable.print(prefix="\t")
print("-")

################################################################

print("\n#### multimedia ####\n")
print("static")
for multimedia in data_lshw._findAllR(id="multimedia"):
	print("\tvendor:", multimedia.vendor)
	print("\tproduct:", multimedia.product)
	print("\tdriver:", multimedia.configuration.driver)
	print("-")

################################################################

print("\n#### network (hardware) ####\n")
print("static")
for network in list(data_lshw._findAllR(id="network")) + list(data_lshw._findAllR(id=re.compile("^network:"))):
	#jk_json.prettyPrint(network._toDict())
	print("\tvendor:", network.vendor)
	print("\tproduct:", network.product)
	print("\tdevice:", network.logicalname)		# network device name
	if network.configuration.link:
		print("\thas_link:", network.configuration.link == "yes")
	else:
		print("\thas_link:", "unknown")
	if network.capabilities.tp:
		# regular twisted pair network

		if network.maxSpeedInBitsPerSecond:
			speed, unit = jk_sysinfo.formatBitsPerSecond(network.maxSpeedInBitsPerSecond)
			print("\tspeed maximum:", speed, unit)					# general speed in bits/s

		if network.configuration.speed:
			print("\tspeed current:", network.configuration.speed)			# current speed
		if network.configuration.duplex:
			print("\tduplex:", network.configuration.duplex)

	elif network.configuration.wireless:
		# regular wireless network

		print("\twireless standard:", network.configuration.wireless)			# "IEEE 802.11"

	else:
		raise Exception("Unknown network type")

	print("\tdescription:", network.description)
	print("\tdriver:", network.configuration.driver)
	print("\tmac_addr:", network.serial)
	print("-")

################################################################

print("\n#### sensors ####\n")

def formatSensorData(data:jk_flexdata.FlexObject) -> str:
	if data._isEmpty():
		return "n/a"
	if data.sensor == "volt":
		return str(data.value) + "V"
	if data.sensor == "fan":
		return str(data.value) + " rpm"
	elif data.sensor == "temp":
		if data.crit and data.max:
			return jk_sysinfo.formatTemperatureGraphC(data.value, data.crit) + " (max: " + str(data.max) + ", crit: " + str(data.crit) + ")"
			#return str(data.value) + " °C (max: " + str(data.max) + ", crit: " + str(data.crit) + ")"
		else:
			return jk_sysinfo.formatTemperatureGraphC(data.value)
			#return str(data.value) + " °C"
	else:
		raise Exception("Unknown: " + repr(data.sensor))
#

print("runtime")
for data in data_sensors._values():
	#jk_json.prettyPrint(data._toDict())
	for sensorItemName, sensorItemStruct in data.sensorData._items():
		print("\t" + data.device + "." + sensorItemName + ": " + formatSensorData(sensorItemStruct))
print("-")

################################################################

print("\n#### network (os) ####\n")
print("runtime")
table = jk_console.SimpleTable()
table.addRow(
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
for networkInterface, networkInterfaceData in data_net_info._items():
	table.addRow(
		networkInterface,
		networkInterfaceData.is_loop,
		networkInterfaceData.is_wlan,
		networkInterfaceData.mac_addr,
		networkInterfaceData.mtu,
		networkInterfaceData.rx_packets,
		networkInterfaceData.rx_dropped,
		networkInterfaceData.rx_errors,
		networkInterfaceData.tx_packets,
		networkInterfaceData.tx_dropped,
		networkInterfaceData.tx_errors,
	)
table.print(prefix="\t")
print("-")

################################################################

print("\n#### drives ####\n")

print("runtime")

@checkFunctionSignature()
def printDevice(data_lsblk:jk_flexdata.FlexObject, data_mounts:jk_flexdata.FlexObject, data_df:jk_flexdata.FlexObject, indent:str=""):
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
			print("Not found: " + data_lsblk.mountpoint)

	if data_lsblk.children:
		for c in data_lsblk.children:
			printDevice(c, data_mounts, data_df, indent)
#

# TODO: drive models

#print(data_lsblk._keys())
for d in data_lsblk.deviceTree:
	printDevice(d, data_mounts, data_df, "\t")
	# TODO: list logical drives
print("-")

################################################################

print()









