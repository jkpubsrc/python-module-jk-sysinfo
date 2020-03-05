

import sys
import re

from jk_cachefunccalls import cacheCalls
#import jk_json

from .parsing_utils import *
from .invoke_utils import run
from .get_ifconfig import get_ifconfig





def _get_network_file_list(c = None) -> dict:
	stdout, _, _ = run(c, "/bin/ls /sys/class/net/*/")
	groupsTemp = [ x.strip().split("\n") for x in stdout.split("\n\n") ]
	groups = {}
	for groupItems in groupsTemp:
		interface = groupItems[0].split("/")[4]
		groups[interface] = groupItems[1:]
	return groups
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
@cacheCalls(seconds=3, dependArgs=[0])
def get_net_info(c = None) -> dict:
	ret = {}

	data = get_ifconfig(c)

	groups = _get_network_file_list(c)
	interfaces = list(groups.keys())

	for interface in interfaces:
		filesAndDirs = groups[interface]

		stdout, _, _ = run(c, "cat /sys/class/net/" + interface + "/address")
		macAddr = stdout.strip()

		stdout, _, _ = run(c, "cat /sys/class/net/" + interface + "/mtu")
		mtu = int(stdout.strip())

		bIsWLAN = "wireless" in filesAndDirs

		data[interface]["mac_addr"] = macAddr
		data[interface]["mtu"] = mtu
		data[interface]["is_wlan"] = bIsWLAN

		for fileName in [ "rx_bytes", "rx_packets", "rx_errors", "rx_dropped", "tx_bytes", "tx_packets", "tx_errors", "tx_dropped" ]:
			stdout, _, _ = run(c, "cat /sys/class/net/" + interface + "/statistics/" + fileName)
			data[interface][fileName] = int(stdout.strip())

		if bIsWLAN:
			stdout, _, _ = run(c, "/sbin/iwlist " + interface + " bitrate")

			"""
			wlp2s0		unknown bit-rate information.
						Current Bit Rate=144.4 Mb/s
			"""

			s = stdout.split("\n")[1].strip()
			if s:
				assert s.startswith("Current Bit Rate")
				pos = s.find("=")
				if pos < 0:
					pos = s.find(":")
					if pos < 0:
						raise Exception("Unexpected data: " + repr(s))
				s = s[pos+1:]
				pos = s.find(" ")
				data[interface]["bitrate_current"] = {
					"value": float(s[:pos]),
					"unit": s[pos+1:].strip(),
				}
			else:
				data[interface]["bitrate_current"] = None

	return data
#














