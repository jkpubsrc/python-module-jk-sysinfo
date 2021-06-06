

import re

from jk_cachefunccalls import cacheCalls

from .parsing_utils import *
from .invoke_utils import run



_parserColonKVP = ParseAtFirstDelimiter(delimiter=":", valueCanBeWrappedInDoubleQuotes=False, keysReplaceSpacesWithUnderscores=False)





# we specify the following pattern in such a tortuous way to be compatible to Python 3.5
_PATTERN_1 = "".join([ x.strip() for x in """
	^
	(?P<inetaddr>inet addr:([^\\s]+))
	(
		\\s+(?P<ptp>P-t-P:([^\\s]+))
	)?
	(
		\\s+(?P<bcast>Bcast:([^\\s]+))
	)?
	\\s+(?P<mask>Mask:([^\\s]+))
	$
""".split("\n") ])








#
# Note: This function is a building block for <c>get_net_info()</c>.
#
# Returns:
#	{
#		"br0": {
#			"hwaddr": "d8:cb:8a:ec:5f:05",
#			"ifname": "br0",
#			"ip4_addr": "192.168.10.10",
#			"ip4_broadcast_addr": "  Bcast:192.168.255.255",
#			"ip4_netmask": "255.255.0.0",
#			"ip6_addr": "fe80::dacb:8aff:feec:5f05/64",
#			"ip6_scope": "Link",
#			"metric": 1,
#			"mtu": 1500,
#			"rx_bytes": 11664556911,
#			"rx_dropped": 5938,
#			"rx_errors": 0,
#			"rx_frame": 0,
#			"rx_overruns": 0,
#			"rx_packetCount": 9803375,
#			"tx_bytes": 1178570750,
#			"tx_carrier": 0,
#			"tx_dropped": 0,
#			"tx_errors": 0,
#			"tx_overruns": 0,
#			"tx_packetCount": 7143430,
#			"tx_queuelen": "1000",
#			"type": "Ethernet"
#		},
#		"enp0s31f6": {
#			"hwaddr": "d8:cb:8a:ec:5f:05",
#			"ifname": "enp0s31f6",
#			"ip6_addr": "fe80::dacb:8aff:feec:5f05/64",
#			"ip6_scope": "Link",
#			"memory": "df000000-df020000",
#			"metric": 1,
#			"mtu": 1500,
#			"rx_bytes": 11894173175,
#			"rx_dropped": 0,
#			"rx_errors": 0,
#			"rx_frame": 0,
#			"rx_overruns": 0,
#			"rx_packetCount": 10302195,
#			"tx_bytes": 1225779865,
#			"tx_carrier": 0,
#			"tx_dropped": 0,
#			"tx_errors": 0,
#			"tx_overruns": 0,
#			"tx_packetCount": 7384311,
#			"tx_queuelen": "1000",
#			"type": "Ethernet"
#		},
#		"lo": {
#			"hwaddr": null,
#			"ifname": "lo",
#			"ip4_addr": "127.0.0.1",
#			"ip4_broadcast_addr": null,
#			"ip4_netmask": "255.0.0.0",
#			"ip6_addr": "::1/128",
#			"ip6_scope": "Host",
#			"metric": 1,
#			"mtu": 65536,
#			"rx_bytes": 6132108,
#			"rx_dropped": 0,
#			"rx_errors": 0,
#			"rx_frame": 0,
#			"rx_overruns": 0,
#			"rx_packetCount": 5508,
#			"tx_bytes": 6132108,
#			"tx_carrier": 0,
#			"tx_dropped": 0,
#			"tx_errors": 0,
#			"tx_overruns": 0,
#			"tx_packetCount": 5508,
#			"tx_queuelen": "1",
#			"type": "Local Loopback"
#		}
#	}
#
def parse_ifconfig(stdout:str, stderr:str, exitcode:int) -> dict:

	if exitcode != 0:
		raise Exception()

	"""
	enp0s31f6: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        ether a6:b5:c4:d3:e2:f1  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        device interrupt 16  memory 0xef300000-ef320000  

	lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
			inet 127.0.0.1  netmask 255.0.0.0
			inet6 ::1  prefixlen 128  scopeid 0x10<host>
			loop  txqueuelen 1000  (Local Loopback)
			RX packets 101707  bytes 11484587 (11.4 MB)
			RX errors 0  dropped 0  overruns 0  frame 0
			TX packets 101707  bytes 11484587 (11.4 MB)
			TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

	wlp2s0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
			inet 192.168.89.183  netmask 255.255.255.0  broadcast 192.168.89.255
			inet6 ........  prefixlen 64  scopeid 0x20<link>
			ether a1:b2:c3:d4:e5:f6  txqueuelen 1000  (Ethernet)
			RX packets 3758562  bytes 3983872988 (3.9 GB)
			RX errors 0  dropped 0  overruns 0  frame 0
			TX packets 1630817  bytes 222286497 (222.2 MB)
			TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

	--------------------------------------------------------------------------------------------------------------------------------
	---- Ubuntu 16.04

	lo        Link encap:Local Loopback  
			inet addr:127.0.0.1  Mask:255.0.0.0
			inet6 addr: ::1/128 Scope:Host
			UP LOOPBACK RUNNING  MTU:65536  Metric:1
			RX packets:3039 errors:0 dropped:0 overruns:0 frame:0
			TX packets:3039 errors:0 dropped:0 overruns:0 carrier:0
			collisions:0 txqueuelen:0 
			RX bytes:9941926 (9.9 MB)  TX bytes:9941926 (9.9 MB)

	venet0    Link encap:UNSPEC  HWaddr 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  
			inet addr:127.0.0.1  P-t-P:127.0.0.1  Bcast:0.0.0.0  Mask:255.255.255.255
			inet6 addr: ::2/128 Scope:Compat
			UP BROADCAST POINTOPOINT RUNNING NOARP  MTU:1500  Metric:1
			RX packets:65050751 errors:0 dropped:0 overruns:0 frame:0
			TX packets:76929410 errors:0 dropped:0 overruns:0 carrier:0
			collisions:0 txqueuelen:0 
			RX bytes:3515170097 (3.5 GB)  TX bytes:3482061899 (3.4 GB)

	venet0:0  Link encap:UNSPEC  HWaddr 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  
			inet addr:82.165.136.239  P-t-P:82.165.136.239  Bcast:82.165.136.239  Mask:255.255.255.255
			UP BROADCAST POINTOPOINT RUNNING NOARP  MTU:1500  Metric:1
	"""

	lines = stdout.strip().split("\n")
	lineGroups = splitAtEmptyLines(lines)

	ret = {}
	for lineGroup in lineGroups:
		line = lineGroup[0].strip()
		m = re.match(r"^([^\s]+)\s+Link encap:(.+?)(\s+HWaddr\s([^\s]+))?$", line)
		if m is None:
			m = re.match(r"^([^\s]+):\s+flags=", line)
			if m is None:
				raise Exception("Failed to parse line: " + repr(line))
		g = m.groups()
		ifname = g[0]

		record = {
			"ifname": ifname,
			"is_loop": False,
			"mac_addr": None,
		}

		if len(g) > 1:
			record["type"] = g[1]
			record["hwaddr"] = g[3]
		ret[ifname] = record

		lineGroup = lineGroup[1:]

		for line in lineGroup:
			line = line.strip()
			if line.startswith("inet "):
				m = re.match(_PATTERN_1, line)
				if m:
					g = m.groupdict()
					record["ip4_addr"] = g["inetaddr"]
					record["ip4_broadcast_addr"] = g["bcast"]
					record["ip4_netmask"] = g["mask"]
				else:
					m = re.match(r"^inet ([^\s]+)\s+netmask\s+([^\s]+)(\s+broadcast\s+([^\s]+))?$", line)
					if m:
						g = m.groups()
						record["ip4_addr"] = g[0]
						record["ip4_netmask"] = g[1]
						record["ip4_broadcast_addr"] = g[3]
					else:
						raise Exception("Failed to parse line: " + repr(line))

			elif line.startswith("inet6 "):
				m = re.match(r"^inet6 addr:\s+([^\s]+)\s+Scope:([^\s]+)$", line)
				if m:
					g = m.groups()
					record["ip6_addr"] = g[0]
					record["ip6_scope"] = g[1]
				else:
					m = re.match(r"^inet6\s+([^\s]+)\s+prefixlen\s+([^\s]+)\s+scopeid\s+([^<]+)<([^\>]+)>*$", line)
					if m:
						g = m.groups()
						record["ip6_addr"] = g[0]
						record["ip6_scope"] = g[3]
					else:
						raise Exception("Failed to parse line: " + repr(line))

			elif line.startswith("ether "):
				m = re.match(r"^ether\s+([^\s]+)\s+txqueuelen\s([^\s]+)\s+(\([^\s]+\))$", line)
				if m is None:
					raise Exception("Failed to parse line: " + repr(line))
				g = m.groups()
				record["mac_addr"] = g[0]

			elif line.startswith("loop "):
				m = re.match(r"^loop\s+txqueuelen\s+([^\s]+)\s+\(Local Loopback\)$", line)
				if m is None:
					raise Exception("Failed to parse line: " + repr(line))
				record["is_loop"] = True

			elif line.startswith("RX "):
				if line.startswith("RX packets:"):
					line = line[len("RX packets:"):]
					lineItems = line.split(" ")
					record["rx_packetCount"] = int(lineItems[0])
					for lineItem in lineItems[1:]:
						m = re.match(r"^([^\s]+):([^\s]+)$", lineItem)
						if m is None:
							raise Exception("Failed to parse line: " + repr(line))
						g = m.groups()
						record["rx_" + g[0]] = int(g[1])
				elif line.startswith("RX bytes:"):
					m = re.match(r"^RX bytes:(\d+)\s+\([^\)]+?\)\s+TX bytes:(\d+)\s+\([^\)]+?\)$", line)
					if m is None:
						raise Exception("Failed to parse line: " + repr(line))
					g = m.groups()
					record["rx_bytes"] = int(g[0])
					record["tx_bytes"] = int(g[1])
				else:
					pass

			elif line.startswith("TX "):
				if line.startswith("TX packets:"):
					line = line[len("TX packets:"):]
					lineItems = line.split(" ")
					record["tx_packetCount"] = int(lineItems[0])
					for lineItem in lineItems[1:]:
						m = re.match(r"^([^\s]+):([^\s]+)$", lineItem)
						if m is None:
							raise Exception("Failed to parse line: " + repr(line))
						g = m.groups()
						record["tx_" + g[0]] = int(g[1])
				else:
					pass

			elif line.startswith("UP "):
				lineItems = line.split("  ")
				for lineItem in lineItems[1:]:
					m = re.match(r"^([^\s]+):([^\s]+)$", lineItem)
					if m is None:
						raise Exception("Failed to parse line: " + repr(line))
					g = m.groups()
					key = g[0]
					if key == "Metric":
						key = "metric"
					elif key == "MTU":
						key = "mtu"
					else:
						raise Exception("Unknown key at " + ifname + ": " + repr(key))
					record[key] = int(g[1])

			elif line.startswith("device "):
				pass

			else:
				lineItems = line.split(" ")
				for lineItem in lineItems[1:]:
					m = re.match(r"^([^\s]+):([^\s]+)$", lineItem)
					if m is None:
						raise Exception("Failed to parse line: " + repr(line))
					g = m.groups()
					key = g[0]
					if key == "txqueuelen":
						key = "tx_queuelen"
					elif key == "Memory":
						key = "memory"
					else:
						raise Exception("Unknown key at " + ifname + ": " + repr(key))
					record[key] = g[1]

	return ret
#



#
# Returns:
#	{
#		"br0": {
#			"hwaddr": "d8:cb:8a:ec:5f:05",
#			"ifname": "br0",
#			"ip4_addr": "192.168.10.10",
#			"ip4_broadcast_addr": "  Bcast:192.168.255.255",
#			"ip4_netmask": "255.255.0.0",
#			"ip6_addr": "fe80::dacb:8aff:feec:5f05/64",
#			"ip6_scope": "Link",
#			"metric": 1,
#			"mtu": 1500,
#			"rx_bytes": 11664556911,
#			"rx_dropped": 5938,
#			"rx_errors": 0,
#			"rx_frame": 0,
#			"rx_overruns": 0,
#			"rx_packetCount": 9803375,
#			"tx_bytes": 1178570750,
#			"tx_carrier": 0,
#			"tx_dropped": 0,
#			"tx_errors": 0,
#			"tx_overruns": 0,
#			"tx_packetCount": 7143430,
#			"tx_queuelen": "1000",
#			"type": "Ethernet"
#		},
#		"enp0s31f6": {
#			"hwaddr": "d8:cb:8a:ec:5f:05",
#			"ifname": "enp0s31f6",
#			"ip6_addr": "fe80::dacb:8aff:feec:5f05/64",
#			"ip6_scope": "Link",
#			"memory": "df000000-df020000",
#			"metric": 1,
#			"mtu": 1500,
#			"rx_bytes": 11894173175,
#			"rx_dropped": 0,
#			"rx_errors": 0,
#			"rx_frame": 0,
#			"rx_overruns": 0,
#			"rx_packetCount": 10302195,
#			"tx_bytes": 1225779865,
#			"tx_carrier": 0,
#			"tx_dropped": 0,
#			"tx_errors": 0,
#			"tx_overruns": 0,
#			"tx_packetCount": 7384311,
#			"tx_queuelen": "1000",
#			"type": "Ethernet"
#		},
#		"lo": {
#			"hwaddr": null,
#			"ifname": "lo",
#			"ip4_addr": "127.0.0.1",
#			"ip4_broadcast_addr": null,
#			"ip4_netmask": "255.0.0.0",
#			"ip6_addr": "::1/128",
#			"ip6_scope": "Host",
#			"metric": 1,
#			"mtu": 65536,
#			"rx_bytes": 6132108,
#			"rx_dropped": 0,
#			"rx_errors": 0,
#			"rx_frame": 0,
#			"rx_overruns": 0,
#			"rx_packetCount": 5508,
#			"tx_bytes": 6132108,
#			"tx_carrier": 0,
#			"tx_dropped": 0,
#			"tx_errors": 0,
#			"tx_overruns": 0,
#			"tx_packetCount": 5508,
#			"tx_queuelen": "1",
#			"type": "Local Loopback"
#		}
#	}
#
@cacheCalls(seconds=3, dependArgs=[0])
def get_ifconfig(c = None) -> dict:
	stdout, stderr, exitcode = run(c, "/sbin/ifconfig -a")
	return parse_ifconfig(stdout, stderr, exitcode)
#







