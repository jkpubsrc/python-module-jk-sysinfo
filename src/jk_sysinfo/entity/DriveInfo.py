

import os
import typing

import jk_typing
import jk_prettyprintobj

from .DrivePartitionInfo import DrivePartitionInfo






class DriveInfo(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, jdata_lsblk_disk:dict, jdata_hdparam_I:dict):
		self.devicePath = jdata_lsblk_disk["dev"]
		self.diskGranularity = jdata_lsblk_disk["phy-sec"]
		self.isHotplug = jdata_lsblk_disk["hotplug"]
		self.model = jdata_lsblk_disk["model"]
		self.isReadOnly = jdata_lsblk_disk["ro"]
		self.isRotational = jdata_lsblk_disk["rota"]
		self.serial = jdata_lsblk_disk["serial"]
		self.size = jdata_lsblk_disk["size"]
		self.transport = jdata_lsblk_disk["tran"]
		self.uuid = jdata_lsblk_disk["uuid"]
		self.vendor = jdata_lsblk_disk["vendor"]

		self.formFactor = jdata_hdparam_I["configuration"]["formFactor"]
		self.nominalMediaRotationRate = jdata_hdparam_I["configuration"]["nominalMediaRotationRate"]
		self.transportHR = jdata_hdparam_I["general"]["transport"]
		self.firmwareRevision = jdata_hdparam_I["general"]["firmwareRevision"]

		#print(repr(jdata_hdparam_I["general"]["serial"]))
		#print(repr(self.serial))
		assert jdata_hdparam_I["general"]["serial"] == self.serial
		
		#print(repr(jdata_hdparam_I["general"]["model"]))
		#print(repr(self.model))
		#second model seems to be more reasonable - skip this test as there might be differences
		#assert jdata_hdparam_I["general"]["model"] == self.model

		self.isNCQSupported = "Native Command Queueing (NCQ)" in jdata_hdparam_I["features"]
		self.isTRIMSupported = False
		for k, v in jdata_hdparam_I["features"].items():
			if k.startswith("Data Set Management TRIM supported"):
				self.isTRIMSupported = v

		self.partitions = []
		if "children" in jdata_lsblk_disk:
			for jchild in jdata_lsblk_disk["children"]:
				self.partitions.append(DrivePartitionInfo(jchild))
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
			"diskGranularity",
			"isHotplug",
			"model",
			"isReadOnly",
			"isRotational",
			"serial",
			"size",
			"transport",
			"uuid",
			"vendor",
			"formFactor",
			"nominalMediaRotationRate",
			"firmwareRevision",
			"transportHR",
			"isNCQSupported",
			"isTRIMSupported",
			"partitions",
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def toJSON(self) -> dict:
		return {
			"devicePath": self.devicePath,
			"diskGranularity": self.diskGranularity,
			"isHotplug": self.isHotplug,
			"model": self.model,
			"isReadOnly": self.isReadOnly,
			"isRotational": self.isRotational,
			"serial": self.serial,
			"size": self.size,
			"transport": self.transport,
			"uuid": self.uuid,
			"vendor": self.vendor,
			"formFactor": self.formFactor,
			"nominalMediaRotationRate": self.nominalMediaRotationRate,
			"firmwareRevision": self.firmwareRevision,
			"transportHR": self.transportHR,
			"isNCQSupported": self.isNCQSupported,
			"isTRIMSupported": self.isTRIMSupported,
			"partitions": [
				x.toJSON() for x in self.partitions
			] if self.partitions else []
		}
	#

#







