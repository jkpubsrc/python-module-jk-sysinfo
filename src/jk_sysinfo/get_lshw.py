

import json
import re

from jk_cachefunccalls import cacheCalls

from .parsing_utils import *
from .invoke_utils import run





def _isObj(data:dict, filter:dict) -> bool:
	assert isinstance(data, dict)
	assert isinstance(filter, dict)

	for k, v in filter.items():
		if k in data:
			# 1st attempt
			v2 = data[k]
			if v != v2:
				return False
		else:
			if k.startswith("_"):
				# 2nd attempt
				k = k[1:]
				if k in data:
					v2 = data[k]
					if v != v2:
						return False
				else:
					return False
			else:
				return False
	return True
#

def _findAllR(d:dict, **kwargs):
	assert isinstance(d, dict)

	for key, data in d.items():
		if isinstance(data, (list, tuple)):
			for e in data:
				if isinstance(e, dict):
					if _isObj(e, kwargs):
						yield e
			for e in data:
				if isinstance(e, dict):
					yield from _findAllR(e, **kwargs)
		elif isinstance(data, dict):
			if _isObj(data, kwargs):
				yield data
			yield from _findAllR(data, **kwargs)
#

#
# Returns:
#	{
#		"capabilities": {
#			"vsyscall32": "32-bit processes"
#		},
#		"children": [
#			{
#				"children": [
#					{
#						"claimed": true,
#						"class": "memory",
#						"description": "System memory",
#						"id": "memory",
#						"physid": "0",
#						"size": 32635547648,
#						"units": "bytes"
#					},
#					{
#						"businfo": "cpu@0",
#						"capabilities": {
#							"3dnowprefetch": true,
#							"abm": true,
#							"acpi": "thermal control (ACPI)",
#							"adx": true,
#							"aes": true,
#							...
#						},
#						"capacity": 3900000000,
#						"claimed": true,
#						"class": "processor",
#						"id": "cpu",
#						"physid": "1",
#						"product": "Intel(R) Core(TM) i5-6600 CPU @ 3.30GHz",
#						"size": 799992000,
#						"units": "Hz",
#						"vendor": "Intel Corp.",
#						"width": 64
#					},
#					{
#						"businfo": "pci@0000:00:00.0",
#						"children": [
#							{
#								"businfo": "pci@0000:00:02.0",
#								"capabilities": {
#									"bus_master": "bus mastering",
#									"cap_list": "PCI capabilities listing",
#									"rom": "extension ROM",
#									"vga_controller": true
#								},
#								"claimed": true,
#								"class": "display",
#								"clock": 33000000,
#								"configuration": {
#									"driver": "i915_bpo",
#									"latency": "0"
#								},
#								"description": "VGA compatible controller",
#								"handle": "PCI:0000:00:02.0",
#								"id": "display",
#								"physid": "2",
#								"product": "HD Graphics 530",
#								"vendor": "Intel Corporation",
#								"version": "06",
#								"width": 64
#							},
#							{
#								"businfo": "pci@0000:00:08.0",
#								"capabilities": {
#									"bus_master": "bus mastering",
#									"cap_list": "PCI capabilities listing"
#								},
#								"class": "generic",
#								"clock": 33000000,
#								"configuration": {
#									"latency": "0"
#								},
#								"description": "System peripheral",
#								"handle": "PCI:0000:00:08.0",
#								"id": "generic:0",
#								"physid": "8",
#								"product": "Xeon E3-1200 v5/v6 / E3-1500 v5 / 6th/7th Gen Core Processor Gaussian Mixture Model",
#								"vendor": "Intel Corporation",
#								"version": "00",
#								"width": 64
#							},
#							{
#								"businfo": "pci@0000:00:14.0",
#								"capabilities": {
#									"bus_master": "bus mastering",
#									"cap_list": "PCI capabilities listing",
#									"xhci": true
#								},
#								"claimed": true,
#								"class": "bus",
#								"clock": 33000000,
#								"configuration": {
#									"driver": "xhci_hcd",
#									"latency": "0"
#								},
#								"description": "USB controller",
#								"handle": "PCI:0000:00:14.0",
#								"id": "usb",
#								"physid": "14",
#								"product": "100 Series/C230 Series Chipset Family USB 3.0 xHCI Controller",
#								"vendor": "Intel Corporation",
#								"version": "31",
#								"width": 64
#							},
#							...,
#							{
#								"businfo": "pci@0000:00:17.0",
#								"capabilities": {
#									"ahci_1.0": true,
#									"bus_master": "bus mastering",
#									"cap_list": "PCI capabilities listing",
#									"storage": true
#								},
#								"claimed": true,
#								"class": "storage",
#								"clock": 66000000,
#								"configuration": {
#									"driver": "ahci",
#									"latency": "0"
#								},
#								"description": "SATA controller",
#								"handle": "PCI:0000:00:17.0",
#								"id": "storage",
#								"physid": "17",
#								"product": "Q170/Q150/B150/H170/H110/Z170/CM236 Chipset SATA Controller [AHCI Mode]",
#								"vendor": "Intel Corporation",
#								"version": "31",
#								"width": 32
#							},
#							...,
#							{
#								"businfo": "pci@0000:00:1f.2",
#								"capabilities": {
#									"bus_master": "bus mastering"
#								},
#								"class": "memory",
#								"clock": 33000000,
#								"configuration": {
#									"latency": "0"
#								},
#								"description": "Memory controller",
#								"handle": "PCI:0000:00:1f.2",
#								"id": "memory",
#								"physid": "1f.2",
#								"product": "100 Series/C230 Series Chipset Family Power Management Controller",
#								"vendor": "Intel Corporation",
#								"version": "31",
#								"width": 32
#							},
#							{
#								"businfo": "pci@0000:00:1f.3",
#								"capabilities": {
#									"bus_master": "bus mastering",
#									"cap_list": "PCI capabilities listing"
#								},
#								"claimed": true,
#								"class": "multimedia",
#								"clock": 33000000,
#								"configuration": {
#									"driver": "snd_hda_intel",
#									"latency": "32"
#								},
#								"description": "Audio device",
#								"handle": "PCI:0000:00:1f.3",
#								"id": "multimedia",
#								"physid": "1f.3",
#								"product": "100 Series/C230 Series Chipset Family HD Audio Controller",
#								"vendor": "Intel Corporation",
#								"version": "31",
#								"width": 64
#							},
#							...,
#							{
#								"businfo": "pci@0000:00:1f.6",
#								"capabilities": {
#									"1000bt-fd": "1Gbit/s (full duplex)",
#									"100bt": "100Mbit/s",
#									"100bt-fd": "100Mbit/s (full duplex)",
#									"10bt": "10Mbit/s",
#									"10bt-fd": "10Mbit/s (full duplex)",
#									"autonegotiation": "Auto-negotiation",
#									"bus_master": "bus mastering",
#									"cap_list": "PCI capabilities listing",
#									"ethernet": true,
#									"physical": "Physical interface",
#									"tp": "twisted pair"
#								},
#								"capacity": 1000000000,
#								"claimed": true,
#								"class": "network",
#								"clock": 33000000,
#								"configuration": {
#									"autonegotiation": "on",
#									"broadcast": "yes",
#									"driver": "e1000e",
#									"driverversion": "3.2.6-k",
#									"duplex": "full",
#									"firmware": "0.7-4",
#									"latency": "0",
#									"link": "yes",
#									"multicast": "yes",
#									"port": "twisted pair",
#									"speed": "1Gbit/s"
#								},
#								"description": "Ethernet interface",
#								"handle": "PCI:0000:00:1f.6",
#								"id": "network",
#								"logicalname": "enp0s31f6",
#								"physid": "1f.6",
#								"product": "Ethernet Connection (2) I219-V",
#								"serial": "d8:cb:8a:ec:5f:05",
#								"size": 1000000000,
#								"units": "bit/s",
#								"vendor": "Intel Corporation",
#								"version": "31",
#								"width": 32
#							}
#						],
#						"claimed": true,
#						"class": "bridge",
#						"clock": 33000000,
#						"description": "Host bridge",
#						"handle": "PCIBUS:0000:00",
#						"id": "pci",
#						"physid": "100",
#						"product": "Xeon E3-1200 v5/E3-1500 v5/6th Gen Core Processor Host Bridge/DRAM Registers",
#						"vendor": "Intel Corporation",
#						"version": "07",
#						"width": 32
#					},
#					{
#						"capabilities": {
#							"emulated": "Emulated device"
#						},
#						"children": [
#							{
#								"businfo": "scsi@3:0.0.0",
#								"capabilities": {
#									"audio": "Audio CD playback",
#									"cd-r": "CD-R burning",
#									"cd-rw": "CD-RW burning",
#									"dvd": "DVD playback",
#									"dvd-r": "DVD-R burning",
#									"dvd-ram": "DVD-RAM burning",
#									"removable": "support is removable"
#								},
#								"children": [
#									{
#										"claimed": true,
#										"class": "disk",
#										"configuration": {
#											"mount.fstype": "iso9660",
#											"mount.options": "ro,nosuid,nodev,relatime,uid=1000,gid=1000,iocharset=utf8,mode=0400,dmode=0500",
#											"state": "mounted"
#										},
#										"dev": "11:0",
#										"id": "medium",
#										"logicalname": [
#											"/dev/cdrom",
#											"/media/xxxxxxxx/YYYYYY"
#										],
#										"physid": "0"
#									}
#								],
#								"claimed": true,
#								"class": "disk",
#								"configuration": {
#									"ansiversion": "5",
#									"mount.fstype": "iso9660",
#									"mount.options": "ro,nosuid,nodev,relatime,uid=1000,gid=1000,iocharset=utf8,mode=0400,dmode=0500",
#									"state": "mounted",
#									"status": "ready"
#								},
#								"description": "DVD-RAM writer",
#								"dev": "11:0",
#								"handle": "SCSI:03:00:00:00",
#								"id": "cdrom",
#								"logicalname": [
#									"/dev/cdrom",
#									"/dev/cdrw",
#									"/dev/dvd",
#									"/dev/dvdrw",
#									"/dev/sr0",
#								],
#								"physid": "0.0.0",
#								"product": "CDDVDW SH-S203P",
#								"vendor": "TSSTcorp",
#								"version": "SB00"
#							}
#						],
#						"claimed": true,
#						"class": "storage",
#						"id": "scsi",
#						"logicalname": "scsi3",
#						"physid": "2"
#					}
#				],
#				"claimed": true,
#				"class": "bus",
#				"description": "Motherboard",
#				"id": "core",
#				"physid": "0"
#			}
#		],
#		"claimed": true,
#		"class": "system",
#		"description": "Computer",
#		"id": "nbxxxxxxxx",
#		"width": 64
#	}
#
def parse_lshw(stdout:str, stderr:str, exitcode:int) -> dict:
	try:
		data_lshw = json.loads(stdout)
	except json.decoder.JSONDecodeError as ee:
		raise Exception("JSON parsing error. Please upgrade lshw as your OS seems to use a very old version of lshw.")

	if isinstance(data_lshw, list):
		assert len(data_lshw) == 1
		data_lshw = data_lshw[0]
	assert isinstance(data_lshw, dict)

	# enrich with additional information: network

	for network in _findAllR(data_lshw, id="network"):
		if ("capabilities" in network) and network["capabilities"].get("tp"):
			# regular twisted pair network

			maxSpeedInBitsPerSecond = None
			for key in network["capabilities"].keys():
				m = re.match(r"^(\d+)bt(-fd)?$", key)
				if m:
					x = int(m.groups()[0]) * 1000000
					if (maxSpeedInBitsPerSecond is None) or (x > maxSpeedInBitsPerSecond):
						maxSpeedInBitsPerSecond = x
			if maxSpeedInBitsPerSecond is None:
				if network.get("size"):
					maxSpeedInBitsPerSecond = int(network["size"])

			if maxSpeedInBitsPerSecond:
				network["maxSpeedInBitsPerSecond"] = maxSpeedInBitsPerSecond

	# enrich with additional information: cpu

	for cpu in _findAllR(data_lshw, id="cpu"):
		if "capabilities" in cpu:
			cpu["hyperthreading"] = "ht" in cpu["capabilities"]
			cpu["virtualization"] = "vmx" in cpu["capabilities"]
			cpu["bitArch"] = 64 if "x86-64" in cpu["capabilities"] else 32
			cpu["encryption"] = "aes" in cpu["capabilities"]

	# return data

	return data_lshw
#



#
# Returns:
#	{
#		"capabilities": {
#			"vsyscall32": "32-bit processes"
#		},
#		"children": [
#			{
#				"children": [
#					{
#						"claimed": true,
#						"class": "memory",
#						"description": "System memory",
#						"id": "memory",
#						"physid": "0",
#						"size": 32635547648,
#						"units": "bytes"
#					},
#					{
#						"businfo": "cpu@0",
#						"capabilities": {
#							"3dnowprefetch": true,
#							"abm": true,
#							"acpi": "thermal control (ACPI)",
#							"adx": true,
#							"aes": true,
#							...
#						},
#						"capacity": 3900000000,
#						"claimed": true,
#						"class": "processor",
#						"id": "cpu",
#						"physid": "1",
#						"product": "Intel(R) Core(TM) i5-6600 CPU @ 3.30GHz",
#						"size": 799992000,
#						"units": "Hz",
#						"vendor": "Intel Corp.",
#						"width": 64
#					},
#					{
#						"businfo": "pci@0000:00:00.0",
#						"children": [
#							{
#								"businfo": "pci@0000:00:02.0",
#								"capabilities": {
#									"bus_master": "bus mastering",
#									"cap_list": "PCI capabilities listing",
#									"rom": "extension ROM",
#									"vga_controller": true
#								},
#								"claimed": true,
#								"class": "display",
#								"clock": 33000000,
#								"configuration": {
#									"driver": "i915_bpo",
#									"latency": "0"
#								},
#								"description": "VGA compatible controller",
#								"handle": "PCI:0000:00:02.0",
#								"id": "display",
#								"physid": "2",
#								"product": "HD Graphics 530",
#								"vendor": "Intel Corporation",
#								"version": "06",
#								"width": 64
#							},
#							{
#								"businfo": "pci@0000:00:08.0",
#								"capabilities": {
#									"bus_master": "bus mastering",
#									"cap_list": "PCI capabilities listing"
#								},
#								"class": "generic",
#								"clock": 33000000,
#								"configuration": {
#									"latency": "0"
#								},
#								"description": "System peripheral",
#								"handle": "PCI:0000:00:08.0",
#								"id": "generic:0",
#								"physid": "8",
#								"product": "Xeon E3-1200 v5/v6 / E3-1500 v5 / 6th/7th Gen Core Processor Gaussian Mixture Model",
#								"vendor": "Intel Corporation",
#								"version": "00",
#								"width": 64
#							},
#							{
#								"businfo": "pci@0000:00:14.0",
#								"capabilities": {
#									"bus_master": "bus mastering",
#									"cap_list": "PCI capabilities listing",
#									"xhci": true
#								},
#								"claimed": true,
#								"class": "bus",
#								"clock": 33000000,
#								"configuration": {
#									"driver": "xhci_hcd",
#									"latency": "0"
#								},
#								"description": "USB controller",
#								"handle": "PCI:0000:00:14.0",
#								"id": "usb",
#								"physid": "14",
#								"product": "100 Series/C230 Series Chipset Family USB 3.0 xHCI Controller",
#								"vendor": "Intel Corporation",
#								"version": "31",
#								"width": 64
#							},
#							...,
#							{
#								"businfo": "pci@0000:00:17.0",
#								"capabilities": {
#									"ahci_1.0": true,
#									"bus_master": "bus mastering",
#									"cap_list": "PCI capabilities listing",
#									"storage": true
#								},
#								"claimed": true,
#								"class": "storage",
#								"clock": 66000000,
#								"configuration": {
#									"driver": "ahci",
#									"latency": "0"
#								},
#								"description": "SATA controller",
#								"handle": "PCI:0000:00:17.0",
#								"id": "storage",
#								"physid": "17",
#								"product": "Q170/Q150/B150/H170/H110/Z170/CM236 Chipset SATA Controller [AHCI Mode]",
#								"vendor": "Intel Corporation",
#								"version": "31",
#								"width": 32
#							},
#							...,
#							{
#								"businfo": "pci@0000:00:1f.2",
#								"capabilities": {
#									"bus_master": "bus mastering"
#								},
#								"class": "memory",
#								"clock": 33000000,
#								"configuration": {
#									"latency": "0"
#								},
#								"description": "Memory controller",
#								"handle": "PCI:0000:00:1f.2",
#								"id": "memory",
#								"physid": "1f.2",
#								"product": "100 Series/C230 Series Chipset Family Power Management Controller",
#								"vendor": "Intel Corporation",
#								"version": "31",
#								"width": 32
#							},
#							{
#								"businfo": "pci@0000:00:1f.3",
#								"capabilities": {
#									"bus_master": "bus mastering",
#									"cap_list": "PCI capabilities listing"
#								},
#								"claimed": true,
#								"class": "multimedia",
#								"clock": 33000000,
#								"configuration": {
#									"driver": "snd_hda_intel",
#									"latency": "32"
#								},
#								"description": "Audio device",
#								"handle": "PCI:0000:00:1f.3",
#								"id": "multimedia",
#								"physid": "1f.3",
#								"product": "100 Series/C230 Series Chipset Family HD Audio Controller",
#								"vendor": "Intel Corporation",
#								"version": "31",
#								"width": 64
#							},
#							...,
#							{
#								"businfo": "pci@0000:00:1f.6",
#								"capabilities": {
#									"1000bt-fd": "1Gbit/s (full duplex)",
#									"100bt": "100Mbit/s",
#									"100bt-fd": "100Mbit/s (full duplex)",
#									"10bt": "10Mbit/s",
#									"10bt-fd": "10Mbit/s (full duplex)",
#									"autonegotiation": "Auto-negotiation",
#									"bus_master": "bus mastering",
#									"cap_list": "PCI capabilities listing",
#									"ethernet": true,
#									"physical": "Physical interface",
#									"tp": "twisted pair"
#								},
#								"capacity": 1000000000,
#								"claimed": true,
#								"class": "network",
#								"clock": 33000000,
#								"configuration": {
#									"autonegotiation": "on",
#									"broadcast": "yes",
#									"driver": "e1000e",
#									"driverversion": "3.2.6-k",
#									"duplex": "full",
#									"firmware": "0.7-4",
#									"latency": "0",
#									"link": "yes",
#									"multicast": "yes",
#									"port": "twisted pair",
#									"speed": "1Gbit/s"
#								},
#								"description": "Ethernet interface",
#								"handle": "PCI:0000:00:1f.6",
#								"id": "network",
#								"logicalname": "enp0s31f6",
#								"physid": "1f.6",
#								"product": "Ethernet Connection (2) I219-V",
#								"serial": "d8:cb:8a:ec:5f:05",
#								"size": 1000000000,
#								"units": "bit/s",
#								"vendor": "Intel Corporation",
#								"version": "31",
#								"width": 32
#							}
#						],
#						"claimed": true,
#						"class": "bridge",
#						"clock": 33000000,
#						"description": "Host bridge",
#						"handle": "PCIBUS:0000:00",
#						"id": "pci",
#						"physid": "100",
#						"product": "Xeon E3-1200 v5/E3-1500 v5/6th Gen Core Processor Host Bridge/DRAM Registers",
#						"vendor": "Intel Corporation",
#						"version": "07",
#						"width": 32
#					},
#					{
#						"capabilities": {
#							"emulated": "Emulated device"
#						},
#						"children": [
#							{
#								"businfo": "scsi@3:0.0.0",
#								"capabilities": {
#									"audio": "Audio CD playback",
#									"cd-r": "CD-R burning",
#									"cd-rw": "CD-RW burning",
#									"dvd": "DVD playback",
#									"dvd-r": "DVD-R burning",
#									"dvd-ram": "DVD-RAM burning",
#									"removable": "support is removable"
#								},
#								"children": [
#									{
#										"claimed": true,
#										"class": "disk",
#										"configuration": {
#											"mount.fstype": "iso9660",
#											"mount.options": "ro,nosuid,nodev,relatime,uid=1000,gid=1000,iocharset=utf8,mode=0400,dmode=0500",
#											"state": "mounted"
#										},
#										"dev": "11:0",
#										"id": "medium",
#										"logicalname": [
#											"/dev/cdrom",
#											"/media/xxxxxxxx/YYYYYY"
#										],
#										"physid": "0"
#									}
#								],
#								"claimed": true,
#								"class": "disk",
#								"configuration": {
#									"ansiversion": "5",
#									"mount.fstype": "iso9660",
#									"mount.options": "ro,nosuid,nodev,relatime,uid=1000,gid=1000,iocharset=utf8,mode=0400,dmode=0500",
#									"state": "mounted",
#									"status": "ready"
#								},
#								"description": "DVD-RAM writer",
#								"dev": "11:0",
#								"handle": "SCSI:03:00:00:00",
#								"id": "cdrom",
#								"logicalname": [
#									"/dev/cdrom",
#									"/dev/cdrw",
#									"/dev/dvd",
#									"/dev/dvdrw",
#									"/dev/sr0",
#									"/media/xxxxxxxx/YYYYYY"
#								],
#								"physid": "0.0.0",
#								"product": "CDDVDW SH-S203P",
#								"vendor": "TSSTcorp",
#								"version": "SB00"
#							}
#						],
#						"claimed": true,
#						"class": "storage",
#						"id": "scsi",
#						"logicalname": "scsi3",
#						"physid": "2"
#					}
#				],
#				"claimed": true,
#				"class": "bus",
#				"description": "Motherboard",
#				"id": "core",
#				"physid": "0"
#			}
#		],
#		"claimed": true,
#		"class": "system",
#		"description": "Computer",
#		"id": "nbxxxxxxxx",
#		"width": 64
#	}
#
@cacheCalls(seconds=3, dependArgs=[0])
def get_lshw(c = None) -> dict:
	stdout, stderr, exitcode = run(c, "/usr/bin/lshw -json")
	return parse_lshw(stdout, stderr, exitcode)
#







