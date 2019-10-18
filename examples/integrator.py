#!/usr/bin/python3


import os
import sys
import re
import time
import json

import jk_sysinfo
import jk_json
import jk_flexdata
import jk_utils
import jk_dirmonitor










systemData = jk_flexdata.createFromData({})

dirMon = jk_dirmonitor.DirectoryMonitor("data/")




while True:
	newFiles, modifiedFiles, unmodifiedFiles, deletedFiles = dirMon.update()

	print("NEW:")
	for item in newFiles:
		print("\t" + str(item))
		identifier = item.name[:-5]
		with open(item.path, "r") as f:
			json_data = json.load(f)
		systemData[identifier] = jk_flexdata.createFromData(json_data)

	print("MODIFIED:")
	for item in modifiedFiles:
		print("\t" + str(item))
		identifier = item.name[:-5]
		with open(item.path, "r") as f:
			json_data = json.load(f)
		systemData[identifier] = jk_flexdata.createFromData(json_data)

	print("DELETED")
	for item in deletedFiles:
		print("\t" + str(item))

	jk_json.saveToFilePretty(list(systemData._toDict().values())[0], "x.json")
	# print(systemData._getByPath(["testsystem", "cpu", "data", "count"]))

	time.sleep(3)





















