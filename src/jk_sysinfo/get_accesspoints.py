

import sys
import re

from jk_cachefunccalls import cacheCalls
#import jk_json

from .parsing_utils import *
from .invoke_utils import run
from .get_net_info import _get_network_file_list





#
# Returns:
#	{
#		"bitrates": [
#			{
#				"unit": "Mb/s",
#				"values": [
#					1.0,
#					2.0,
#					5.5,
#					11.0,
#					6.0,
#					9.0,
#					12.0,
#					18.0,
#					24.0,
#					36.0,
#					48.0,
#					54.0
#				]
#			}
#		],
#		"encrypted": true,
#		"encryption": {
#			"IEEE 802.11i/WPA2 Version 1": {
#				"Authentication Suites (1)": "PSK",
#				"Group Cipher": "CCMP",
#				"Pairwise Ciphers (1)": "CCMP"
#			}
#		},
#		"essid": "HotelChernoMore",
#		"frequency": {
#			"channel": 11,
#			"unit": "GHz",
#			"value": 2.462
#		},
#		"mac": "F0:9F:C2:91:E3:1D",
#		"signal": {
#			"quality_cur": 52,
#			"quality_max": 70,
#			"signal_level": {
#				"unit": "dBm",
#				"value": -58
#			}
#		}
#	}
#
def __parse_single_wifi_cell(interface:str, radioCellLines:list, radioCellLinesIE:list):
	ret = {
		"essid": None
	}

	for line in radioCellLines:

		# "Frequency:2.412 GHz (Channel 1)"
		m = re.match(r"^Frequency:([\d\.]+)\s+([MGT]Hz)\s+\(Channel\s+(\d+)\)$", line)
		if m:
			groups = m.groups()
			ret["frequency"] = {
				"value": float(groups[0]),
				"unit": groups[1],
				"channel": int(groups[2]),
			}
			continue

		# "Address: E4:8D:8C:6D:C3:F5"
		m = re.match(r"^Address:\s+(.*)$", line)
		if m:
			groups = m.groups()
			ret["mac"] = groups[0]

		# "Channel:1"

		# "Quality=63/70  Signal level=-47 dBm  "
		m = re.match(r"^Quality=(\d+)/(\d+)\s+Signal\s+level=([-\d]+)\s+dBm\s+$", line)
		if m:
			groups = m.groups()
			ret["signal"] = {
				"quality_cur": int(groups[0]),
				"quality_max": int(groups[1]),
				"signal_level": {
					"value": int(groups[2]),
					"unit": "dBm",
				}
			}

		# "Encryption key:on"
		m = re.match(r"^Encryption\s+key:(.*)$", line)
		if m:
			groups = m.groups()
			ret["encrypted"] = groups[0] == "on"

		# "ESSID:\"ConfHall 1,2\""
		m = re.match(r"^ESSID:\"(.+)\"$", line)
		if m:
			groups = m.groups()
			ret["essid"] = groups[0]

		# "Bit Rates:1 Mb/s; 2 Mb/s; 5.5 Mb/s; 11 Mb/s; 6 Mb/s	  9 Mb/s; 12 Mb/s; 18 Mb/s"
		# "Bit Rates:24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s"
		m = re.match(r"^Bit Rates:(.*)$", line)
		if m:
			bitrates = ret.get("bitrates")
			if bitrates is None:
				bitrates = []
				ret["bitrates"] = bitrates

			# "1 Mb/s; 2 Mb/s; 5.5 Mb/s; 11 Mb/s; 6 Mb/s	  9 Mb/s; 12 Mb/s; 18 Mb/s"
			items = re.split(";|\s\s\s", str(m.groups()[0]))
			for item in items:
				item = item.strip()
				if item:
					# "12 MB/s"
					m = re.match(r"^\s*([\.\d]+)\s+([GM]b/s)\s*$", item)
					if m:
						groups = m.groups()
						bitrates.append({
							"value": float(groups[0]),
							"unit": groups[1],
						})
					else:
						raise Exception("Failed to match: " + repr(item))


		# "Mode:Master"

		# "Extra:tsf=000000411f6f43d8"

		# "Extra: Last beacon: 4364ms ago"
		#m = re.match(r"^$", line)
		#if m:
		#	groups = m.groups()
		#	ret["mac"] = groups[0]

	ret["bitrates"] = simplifyValueList(ret["bitrates"])

	# now process the rest of the data

	radioCellDictIE = {}
	for key, values in groupLinesByLeadingSpace(radioCellLinesIE).items():
		if key.startswith("IE: "):
			key = key[4:]
			if not key.startswith("Unknown: "):
				radioCellDictIE[key] = values
		else:
			raise Exception("Unexpected key: " + repr(key))

	"""
	{
	"IEEE 802.11i/WPA2 Version 1": [
		"Group Cipher : TKIP",
		"Pairwise Ciphers (2) : CCMP TKIP",
		"Authentication Suites (1) : PSK"
	],
	"WPA Version 1": [
		"Group Cipher : TKIP",
		"Pairwise Ciphers (2) : CCMP TKIP",
		"Authentication Suites (1) : PSK"
	]
	}
	"""

	encryptionData = {}
	for key, lines in radioCellDictIE.items():
		encryptionSchemaData = {}
		for line in lines:
			pos = line.find(" : ")
			if pos < 0:
				raise Exception("Unexpected line: " + repr(line))
			encryptionSchemaData[line[:pos].strip()] = line[pos+3:].strip()
		encryptionData[key] = encryptionSchemaData

	ret["encryption"] = encryptionData

	return ret
#

#
# Returns:
#	[
#		"0": {
#			"bitrates": [
#				{
#					"unit": "Mb/s",
#					"values": [
#						1.0,
#						2.0,
#						5.5,
#						11.0,
#						6.0,
#						9.0,
#						12.0,
#						18.0,
#						24.0,
#						36.0,
#						48.0,
#						54.0
#					]
#				}
#			],
#			"encrypted": true,
#			"encryption": {
#				"IEEE 802.11i/WPA2 Version 1": {
#					"Authentication Suites (1)": "PSK",
#					"Group Cipher": "CCMP",
#					"Pairwise Ciphers (1)": "CCMP"
#				}
#			},
#			"essid": "HotelChernoMore",
#			"frequency": {
#				"channel": 11,
#				"unit": "GHz",
#				"value": 2.462
#			},
#			"mac": "F0:9F:C2:91:E3:1D",
#			"signal": {
#				"quality_cur": 52,
#				"quality_max": 70,
#				"signal_level": {
#					"unit": "dBm",
#					"value": -58
#				}
#			}
#		},
#		...
#	]
#
def __get_accesspoints_for_interface(interface:str, c = None, runAsRoot:bool = False) -> list:
	if runAsRoot:
		stdout, _, _x = run(c, "sudo -n /sbin/iwlist " + interface + " scan")
	else:
		stdout, _, _ = run(c, "/sbin/iwlist " + interface + " scan")
	lines = stdout.strip().split("\n")

	"""
	wlp2s0	Scan completed :
			Cell 01 - Address: F0:9F:C2:91:E3:1D
						Channel:11
						Frequency:2.462 GHz (Channel 11)
						Quality=51/70  Signal level=-59 dBm  
						Encryption key:on
						ESSID:"HotelChernoMore"
						Bit Rates:1 Mb/s; 2 Mb/s; 5.5 Mb/s; 11 Mb/s; 6 Mb/s
								9 Mb/s; 12 Mb/s; 18 Mb/s
						Bit Rates:24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s
						Mode:Master
						Extra:tsf=00000450e91d6016
						Extra: Last beacon: 3816ms ago
						IE: Unknown: 000F486F74656C436865726E6F4D6F7265
						IE: Unknown: 010882848B968C129824
						IE: Unknown: 03010B
						IE: Unknown: 2A0100
						IE: Unknown: 3204B048606C
						IE: Unknown: 0B050500630000
						IE: Unknown: 2D1AAC0103FFFF000000000000000000000100000000000000000000
						IE: Unknown: 3D160B000D00000000000000000000000000000000000000
						IE: Unknown: 7F080000000000000040
						IE: Unknown: DD180050F2020101000003A4000027A4000042435E0062322F00
						IE: Unknown: DD0900037F01010000FF7F
						IE: Unknown: DD0A00037F04010008000A00
						IE: Unknown: DD1300156D00010100010282E58106F09FC290E31D
						IE: IEEE 802.11i/WPA2 Version 1
							Group Cipher : CCMP
							Pairwise Ciphers (1) : CCMP
							Authentication Suites (1) : PSK
			Cell 02 - Address: F2:9F:C2:91:E1:9F
						Channel:1
						Frequency:2.412 GHz (Channel 1)
						Quality=32/70  Signal level=-78 dBm  
						Encryption key:on
						ESSID:""
						Bit Rates:1 Mb/s; 2 Mb/s; 5.5 Mb/s; 11 Mb/s; 6 Mb/s
								9 Mb/s; 12 Mb/s; 18 Mb/s
						Bit Rates:24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s
						Mode:Master
						Extra:tsf=0000040115180180
						Extra: Last beacon: 20328ms ago
						IE: Unknown: 0000
						IE: Unknown: 010882848B968C129824
						IE: Unknown: 030101
						IE: Unknown: 050402030000
						IE: Unknown: 2A0100
						IE: Unknown: 3204B048606C
						IE: Unknown: 0B050000530000
						IE: Unknown: 2D1AAC0103FFFF000000000000000000000100000000000000000000
						IE: Unknown: 3D1601080C00000000000000000000000000000000000000
						IE: Unknown: 7F080000000000000040
						IE: Unknown: DD180050F2020101000003A4000027A4000042435E0062322F00
						IE: Unknown: DD0900037F01010000FF7F
						IE: Unknown: DD0A00037F04010008000A00
						IE: Unknown: DD1600156D00010128010282E58106F09FC290E19F820100
						IE: IEEE 802.11i/WPA2 Version 1
							Group Cipher : CCMP
							Pairwise Ciphers (1) : CCMP
							Authentication Suites (1) : PSK
			...
			Cell 15 - Address: F0:9F:C2:7E:2D:76
						Channel:36
						Frequency:5.18 GHz (Channel 36)
						Quality=34/70  Signal level=-76 dBm  
						Encryption key:on
						ESSID:"HotelChernoMore"
						Bit Rates:6 Mb/s; 9 Mb/s; 12 Mb/s; 18 Mb/s; 24 Mb/s
								36 Mb/s; 48 Mb/s; 54 Mb/s
						Mode:Master
						Extra:tsf=00000450e502e841
						Extra: Last beacon: 3672ms ago
						IE: Unknown: 000F486F74656C436865726E6F4D6F7265
						IE: Unknown: 01088C129824B048606C
						IE: Unknown: 030124
						IE: Unknown: 200103
						IE: Unknown: 0B050000050000
						IE: Unknown: 2D1AEF091BFFFF000000000000000000000100000000000000000000
						IE: Unknown: 3D1624050D00000000000000000000000000000000000000
						IE: Unknown: 7F080000000000000040
						IE: Unknown: BF0CB2018033FAFF0000FAFF0000
						IE: Unknown: C005000000FCFF
						IE: Unknown: C30402D8D8D8
						IE: Unknown: DD180050F2020101000003A4000027A4000042435E0062322F00
						IE: Unknown: DD0900037F01010000FF7F
						IE: Unknown: DD1300156D00010100010217E58106F09FC27C2D76
						IE: IEEE 802.11i/WPA2 Version 1
							Group Cipher : CCMP
							Pairwise Ciphers (1) : CCMP
							Authentication Suites (1) : PSK
	"""

	assert lines[0].find("Scan completed") > 0
	lines = lines[1:]

	lines = removeAllCommonLeadingSpaces(lines)

	radioCellDict = groupLinesByLeadingSpace(lines)

	byESSID = {}
	withoutESSID = []
	n = 0
	for key, lines in radioCellDict.items():
		# key is something like this: "Cell 01 - Address: F0:9F:C2:91:E3:1D"

		# now process the first line and split it
		pos = key.index(" - ")
		cellKey = key[:pos].strip()
		addressPart = key[pos+3:]

		# append lines starting with spaces to the corresponding previous line
		lines2 = []
		lines3 = []
		lastLine = None
		bAddAll = False
		for line in lines:
			if bAddAll:
				lines3.append(line)
				continue

			if line.startswith("IE: "):
				# stop processing here: these lines come last
				if lastLine is not None:
					lines2.append(lastLine)
					lastLine = None
				bAddAll = True
				continue

			if lastLine is None:
				lastLine = line
			else:
				if line[0].isspace():
					lastLine += line
				else:
					lines2.append(lastLine)
					lastLine = line
		assert lastLine is None

		# group everything together
		d = __parse_single_wifi_cell(interface, [ addressPart ] + lines2, lines3)
		n += 1

		essid = d.get("essid")
		if essid is None:
			withoutESSID.append(d)
		else:
			essidList = byESSID.get(essid)
			if essidList is None:
				essidList = []
				byESSID[essid] = essidList
			essidList.append(d)

	"""
	{
	"0": [
		"Address: 18:E8:29:AB:FA:0C",
		"Channel:36",
		"Frequency:5.18 GHz (Channel 36)",
		"Quality=53/70  Signal level=-57 dBm  ",
		"Encryption key:on",
		"ESSID:\"ConfHall 1+\"",
		"Bit Rates:6 Mb/s; 9 Mb/s; 12 Mb/s; 18 Mb/s; 24 Mb/s	  36 Mb/s; 48 Mb/s; 54 Mb/s",
		"Mode:Master",
		"Extra:tsf=000000380c212954",
		"Extra: Last beacon: 3764ms ago",
		"IE: Unknown: 01088C129824B048606C",
		"IE: Unknown: 030124",
		"IE: Unknown: 200103",
		"IE: Unknown: 0B050700080000",
		"IE: Unknown: 2D1AEF091BFFFF000000000000000000000100000000000000000000",
		"IE: Unknown: 3D16240D0C00000000000000000000000000000000000000",
		"IE: Unknown: 7F080000000000000040",
		"IE: Unknown: BF0CB2018033FAFF0000FAFF0000",
		"IE: Unknown: C005000000FCFF",
		"IE: Unknown: C30402D8D8D8",
		"IE: Unknown: DD180050F2020101000003A4000027A4000042435E0062322F00",
		"IE: Unknown: DD0900037F01010000FF7F",
		"IE: Unknown: DD1300156D00010100010217E5810618E829A9FA0C",
		"IE: IEEE 802.11i/WPA2 Version 1",
		"    Group Cipher : CCMP",
		"    Pairwise Ciphers (1) : CCMP",
		"    Authentication Suites (1) : PSK"
	],
		...,
	"2": [
		"Address: E4:8D:8C:6D:C3:F5",
		"Channel:1",
		"Frequency:2.412 GHz (Channel 1)",
		"Quality=63/70  Signal level=-47 dBm  ",
		"Encryption key:on",
		"ESSID:\"ConfHall 1,2\"",
		"Bit Rates:1 Mb/s; 2 Mb/s; 5.5 Mb/s; 11 Mb/s; 6 Mb/s	  9 Mb/s; 12 Mb/s; 18 Mb/s",
		"Bit Rates:24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s",
		"Mode:Master",
		"Extra:tsf=000000411f6f43d8",
		"Extra: Last beacon: 4364ms ago",
		"IE: Unknown: 010882848B960C121824",
		"IE: Unknown: 030101",
		"IE: Unknown: 2A0100",
		"IE: Unknown: 2D1A6E1003FFFF000000000000000000000000000000000000000000",
		"IE: IEEE 802.11i/WPA2 Version 1",
		"    Group Cipher : CCMP",
		"    Pairwise Ciphers (2) : CCMP TKIP",
		"    Authentication Suites (1) : PSK",
		"IE: Unknown: 32043048606C",
		"IE: Unknown: 3D1601050000000000000000000000000000000000000000",
		"IE: Unknown: DD2A000C42000000011E0010000004661E060000453438443843364443334635000000000000000005026C09",
		"IE: WPA Version 1",
		"    Group Cipher : CCMP",
		"    Pairwise Ciphers (2) : CCMP TKIP",
		"    Authentication Suites (1) : PSK",
		"IE: Unknown: DD180050F2020101000003A4000027A4000042435E0062322F00",
		"IE: Unknown: DD1E00904C336E1003FFFF000000000000000000000000000000000000000000",
		"IE: Unknown: DD1A00904C3401050000000000000000000000000000000000000000"
	],
		...
	}
	"""

	return {
		"byESSID": byESSID,
		"withoutESSID": withoutESSID
	}
	return radioCellDict
#

#
# Retrieve network information.
#
# Note: this function makes use of <c>get_ifconfig()</c> and adds more data. If you invoke <c>get_net_info()</c> there is no need to invoke <c>get_ifconfig()</c> any more.
#
# Returns:
#	{
#		"enp0s31f6": {
#			"ifname": "enp0s31f6",
#			"is_wlan": false,
#			"mac_addr": "a6:b5:c4:d3:e2:f1",
#			"mtu": 1500
#		},
#		"lo": {
#			"ifname": "lo",
#			"ip4_addr": "127.0.0.1",
#			"ip4_broadcastAddr": null,
#			"ip4_netmask": "255.0.0.0",
#			"ip6_addr": "::1",
#			"ip6_scope": "host",
#			"is_wlan": false,
#			"mac_addr": "00:00:00:00:00:00",
#			"mtu": 65536
#		},
#		"wlp2s0": {
#			"ifname": "wlp2s0",
#			"ip4_addr": "192.168.99.123",
#			"ip4_broadcastAddr": "192.168.99.255",
#			"ip4_netmask": "255.255.255.0",
#			"ip6_addr": "........",
#			"ip6_scope": "link",
#			"is_wlan": true,
#			"mac_addr": "a1:b2:c3:d4:e5:f6",
#			"mtu": 1500
#		}
#	}
#
#@cacheCalls(seconds=3, dependArgs=[0, 1])		# TODO: we need to fix a bug in cacheCalls first: "IndexError: tuple index out of range" at "cacheCalls.py:45 wrapped    # extraIdentifier += "|" + str(id(args[i]))"
def get_accesspoints(c = None, runAsRoot:bool = False) -> dict:
	ret = {}

	groups = _get_network_file_list(c)
	interfaces = list(groups.keys())

	ret = {}

	for interface in interfaces:
		filesAndDirs = groups[interface]
		if "wireless" in filesAndDirs:
			ret[interface] = __get_accesspoints_for_interface(interface, c, runAsRoot)

	return ret
#














