

import copy
import json

from jk_cachefunccalls import cacheCalls

from .parsing_utils import *
from .invoke_utils import run



_parserColonKVP = ParseAtFirstDelimiter(delimiter="=", valueCanBeWrappedInDoubleQuotes=True)



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
#				"label": "YYYYYY",
#				"mountpoint": "/media/xxxxxxxx/YYYYYY",
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
#			"/media/xxxxxxxx/YYYYYY": {
#				"dev": "/dev/sr0",
#				"fstype": "iso9660",
#				"label": "YYYYYY",
#				"mountPoint": "/media/xxxxxxxx/YYYYYY",
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
			{"name": "sr0", "fstype": "iso9660", "label": "YYYYYY", "uuid": "2001-10-05-02-59-13-00", "mountpoint": "/media/xxxxxxxx/YYYYYY"}
		]
	}
	"""

	if exitcode != 0:
		raise Exception()

	ret = json.loads(stdout.strip())["blockdevices"]
	mountPointMap = {}
	for jBlockDevice in ret:
		__parse_lsblk_postproces_dev(jBlockDevice, mountPointMap)

	return {
		"deviceTree": ret,
		"mountPoints": mountPointMap,
	}
#

def __parse_lsblk_postproces_dev(j, mountPointMap):
	j["dev"] = j["name"]
	if "children" in j:
		for j2 in j["children"]:
			__parse_lsblk_postproces_dev(j2, mountPointMap)
	if j["vendor"]:
		j["vendor"] = j["vendor"].strip()
	if j["mountpoint"]:
		j2 = copy.deepcopy(j)
		if "children" in j2:
			del j2["children"]
		mountPointMap[j2["mountpoint"]] = j2
#

class _LsBlkDevTreeFilter(object):

	def __init__(self, **filterElements) -> None:
		if not filterElements:
			raise Exception("No filter elements specified!")

		self.__jFilter = {}
		for fe_key, fe_valueOrValues in filterElements.items():
			assert isinstance(fe_key, str)

			if isinstance(fe_valueOrValues, (int,str,bool)):
				pass
			elif isinstance(fe_valueOrValues, (list, tuple)):
				for v in fe_valueOrValues:
					if not isinstance(v, (int,str,bool)):
						raise Exception("Filter " + fe_key + " has a value of invalid type!")
			else:
				raise Exception("Filter " + fe_key + " has a value of invalid type!")

			self.__jFilter[fe_key] = fe_valueOrValues
	#

	def checkAccept(self, jData:dict) -> bool:
		for filterKey, filterValueOrValues in self.__jFilter.items():

			jDataValue = jData.get(filterKey, None)
			if jDataValue is None:
				# required key-value-pair does not exist or value is (null)
				return False
			if isinstance(filterValueOrValues, (tuple,list)):
				if jDataValue not in filterValueOrValues:
					# value is not in list of allowed values
					return False
			else:
				if jDataValue != filterValueOrValues:
					# value is not an allowed value
					return False

		return True
	#

#

def filter_lsblk_devtree(jsonRawData:dict, **filterElements) -> list:
	if ("deviceTree" not in jsonRawData) or ("mountPoints" not in jsonRawData):
		raise Exception("Specified data is no JSON raw data!")

	j = jsonRawData["deviceTree"]
	assert isinstance(j, list)

	filter = _LsBlkDevTreeFilter(**filterElements)

	ret = []
	for jitem in j:
		if filter.checkAccept(jitem):
			ret.append(jitem)

	return ret
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
#				"label": "YYYYYY",
#				"mountpoint": "/media/xxxxxxxx/YYYYYY",
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
#			"/media/xxxxxxxx/YYYYYY": {
#				"dev": "/dev/sr0",
#				"fstype": "iso9660",
#				"label": "YYYYYY",
#				"mountPoint": "/media/xxxxxxxx/YYYYYY",
#				"name": "sr0",
#				"uuid": "2001-10-05-02-59-13-00"
#			}
#		}
#	}
#
@cacheCalls(seconds=3, dependArgs=[0])
def get_lsblk(c = None) -> dict:
	stdout, stderr, exitcode = run(c, "/bin/lsblk -bJpO")
	return parse_lsblk(stdout, stderr, exitcode)
#










