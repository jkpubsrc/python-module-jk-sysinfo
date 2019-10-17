

import copy
import json

from .parsing_utils import *
from .invoke_utils import run



_parserColonKVP = ParseAtFirstDelimiter(delimiter="=", valueCanBeWrappedInDoubleQuotes=True)



#
# Returns:
#
#	{
#		"deviceTree": [
#			{
#				"children": [
#					{
#						"dev": "/dev/sda1",
#						"fstype": "ext4",
#						"label": null,
#						"mountpoint": "/",
#						"name": "sda1",
#						"uuid": "94933739-97e5-47e8-b7e8-ab8b7ed3f2a7"
#					}
#				],
#				"dev": "/dev/sda",
#				"fstype": null,
#				"label": null,
#				"mountpoint": null,
#				"name": "sda",
#				"uuid": null
#			},
#			{
#				"dev": "/dev/sr0",
#				"fstype": "iso9660",
#				"label": "BROODWAR",
#				"mountpoint": "/media/woodoo/BROODWAR",
#				"name": "sr0",
#				"uuid": "2001-10-05-02-59-13-00"
#			}
#		],
#		"mountPoints": {
#			"/": {
#				"dev": "/dev/sda1",
#				"fstype": "ext4",
#				"label": null,
#				"mountpoint": "/",
#				"name": "sda1",
#				"uuid": "94933739-97e5-47e8-b7e8-ab8b7ed3f2a7"
#			},
#			"/media/woodoo/BROODWAR": {
#				"dev": "/dev/sr0",
#				"fstype": "iso9660",
#				"label": "BROODWAR",
#				"mountPoint": "/media/woodoo/BROODWAR",
#				"name": "sr0",
#				"uuid": "2001-10-05-02-59-13-00"
#			}
#		}
#	}
#
def parse_lsblk(stdout:str, stderr:str, exitcode:int) -> dict:

	"""
	{
		"blockdevices": [
			{"name": "sda", "fstype": null, "label": null, "uuid": null, "mountpoint": null,
				"children": [
				{"name": "sda1", "fstype": "ext4", "label": null, "uuid": "94933739-97e5-47e8-b7e8-ab8b7ed3f2a7", "mountpoint": "/"}
				]
			},
			{"name": "sr0", "fstype": "iso9660", "label": "BROODWAR", "uuid": "2001-10-05-02-59-13-00", "mountpoint": "/media/woodoo/BROODWAR"}
		]
	}
	"""

	if exitcode != 0:
		raise Exception()

	ret = json.loads(stdout.strip())["blockdevices"]
	mountPointMap = {}
	for jBlockDevice in ret:
		__postproces_lsblk_dev(jBlockDevice, mountPointMap)

	return {
		"deviceTree": ret,
		"mountPoints": mountPointMap,
	}
#

def __postproces_lsblk_dev(j, mountPointMap):
	j["dev"] = j["name"]
	if "children" in j:
		for j2 in j["children"]:
			__postproces_lsblk_dev(j2, mountPointMap)
	if j["mountpoint"]:
		j2 = copy.deepcopy(j)
		if "children" in j2:
			del j2["children"]
		mountPointMap[j2["mountpoint"]] = j2
#



#
# Returns:
#
#	{
#		"devtree": [
#			{
#				"children": [
#					{
#						"dev": "/dev/sda1",
#						"fstype": "ext4",
#						"label": null,
#						"mountpoint": "/",
#						"name": "sda1",
#						"uuid": "94933739-97e5-47e8-b7e8-ab8b7ed3f2a7"
#					}
#				],
#				"dev": "/dev/sda",
#				"fstype": null,
#				"label": null,
#				"mountpoint": null,
#				"name": "sda",
#				"uuid": null
#			},
#			{
#				"dev": "/dev/sr0",
#				"fstype": "iso9660",
#				"label": "BROODWAR",
#				"mountpoint": "/media/woodoo/BROODWAR",
#				"name": "sr0",
#				"uuid": "2001-10-05-02-59-13-00"
#			}
#		],
#		"mountpoints": {
#			"/": {
#				"dev": "/dev/sda1",
#				"fstype": "ext4",
#				"label": null,
#				"mountpoint": "/",
#				"name": "sda1",
#				"uuid": "94933739-97e5-47e8-b7e8-ab8b7ed3f2a7"
#			},
#			"/media/woodoo/BROODWAR": {
#				"dev": "/dev/sr0",
#				"fstype": "iso9660",
#				"label": "BROODWAR",
#				"mountPoint": "/media/woodoo/BROODWAR",
#				"name": "sr0",
#				"uuid": "2001-10-05-02-59-13-00"
#			}
#		}
#	}
#
def get_lsblk(c = None) -> dict:
	stdout, stderr, exitcode = run(c, "/bin/lsblk -bJpO")
	return parse_lsblk(stdout, stderr, exitcode)
#










