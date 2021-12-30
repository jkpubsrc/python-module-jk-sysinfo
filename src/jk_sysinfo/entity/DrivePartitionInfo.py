

import os
import typing

import jk_typing
import jk_utils
import jk_json
import jk_prettyprintobj







class DrivePartitionInfo(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, jdata_lsblk_disk:dict):
		assert jdata_lsblk_disk["type"] == "part"

		self.devicePath = jdata_lsblk_disk["dev"]
		self.fsavail = jdata_lsblk_disk["fsavail"]
		self.fssize = jdata_lsblk_disk["fssize"]
		self.fsused = jdata_lsblk_disk["fsused"]
		self.fstype = jdata_lsblk_disk["fstype"]
		self.mountpoint = jdata_lsblk_disk["mountpoint"]
		self.partflags = jdata_lsblk_disk["partflags"]
		self.parttype = jdata_lsblk_disk["parttype"]
		self.partlabel = jdata_lsblk_disk["partlabel"]
		self.partuuid = jdata_lsblk_disk["partuuid"]
		self.ptuuid = jdata_lsblk_disk["ptuuid"]
		self.uuid = jdata_lsblk_disk["uuid"]
		self.size = jdata_lsblk_disk["size"]
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"devicePath",
			"fsavail",
			"fssize",
			"fsused",
			"fstype",
			"mountpoint",
			"partflags",
			"parttype",
			"partlabel",
			"partuuid",
			"ptuuid",
			"uuid",
			"size",
			"formFactor",
			"nominalMediaRotationRate",
			"firmwareRevision",
			"transportHR",
			"isNCQSupported",
			"isTRIMSupported",
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def toJSON(self) -> dict:
		return {
			"devicePath": self.devicePath,
			"fsavail": self.fsavail,
			"fssize": self.fssize,
			"fsused": self.fsused,
			"fstype": self.fstype,
			"mountpoint": self.mountpoint,
			"partflags": self.partflags,
			"parttype": self.parttype,
			"partlabel": self.partlabel,
			"partuuid": self.partuuid,
			"ptuuid": self.ptuuid,
			"uuid": self.uuid,
			"size": self.size,
		}
	#

#







