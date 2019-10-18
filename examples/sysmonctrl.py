#!/usr/bin/python3


from __future__ import print_function
import os
import sys
import re
import time
import json

from jk_argparsing import *
import jk_sysinfo
#import jk_json
#import jk_flexdata
import jk_utils

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
#

c = None









PRETTY = False
#PRETTY = True



RETRIEVERS = (
	( "lsb_release_a", jk_sysinfo.get_lsb_release_a),
	( "lshw", jk_sysinfo.get_lshw),
	( "mobo", jk_sysinfo.get_motherboard_info),
	( "bios", jk_sysinfo.get_bios_info),
	( "proccpu", jk_sysinfo.get_proc_cpu_info),
	( "cpu", jk_sysinfo.get_cpu_info),
	( "sensors", jk_sysinfo.get_sensors),
	( "sysload", jk_sysinfo.get_proc_load_avg),
	( "mem", jk_sysinfo.get_proc_meminfo),
	( "lsblk", jk_sysinfo.get_lsblk),
	( "reboot", jk_sysinfo.get_needs_reboot),
	( "mounts", jk_sysinfo.get_mount),
	( "df", jk_sysinfo.get_df),
	( "net_info", jk_sysinfo.get_net_info),
	( "uptime", jk_sysinfo.get_uptime),
)





ap = ArgsParser("sysmonctrl", "When invoked this program will retrieve information about the current system and write it to STDOUT.")

ap.optionDataDefaults.set("help", False)

ap.createOption('h', 'help', "Display this help text.").onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("help", True)

ap.createCommand("sysinfo", "Retrieve information about the current system and write it to STDOUT.")	#.expectString("host_identifier", minLength=1)

ap.createAuthor("Jürgen Knauth", "jk@binary-overflow.de")
ap.setLicense("apache", YEAR = 2017, COPYRIGHTHOLDER = "Jürgen Knauth")

ap.createReturnCode(0, "Everything is okay.")
ap.createReturnCode(1, "An error occurred.")

parsedArgs = ap.parse()

bProcessed = False
for command, commandArgs in parsedArgs.parseCommands():
	bProcessed = True

	data = {}
	tAll = time.time()
	for key, retriever in RETRIEVERS:
		t = time.time()
		try:
			v = retriever(c)
		except Exception as ee:
			eprint("ERROR @ " + key)
			v = None
		dt = time.time() - t
		#if isinstance(v, (list, tuple)):
		#	v = [ jk_flexdata.createFromData(x) for x in v ]
		#else:
		#	v = jk_flexdata.createFromData(v)
		data[key] = {
			"_duration": dt,
			"data": v,
			"_t": t,
		}
	dtAll = time.time() - tAll
	data["_t"] = tAll
	data["_duration"] = dtAll

	if PRETTY:
		s = json.dumps(data, indent="\t")
	else:
		s = json.dumps(data)

	print(s)
	#with jk_utils.file_rw.openWriteText("data/" + SYSTEM_ID + ".json", bSafeWrite=True) as f:
	#	f.write(s)

	break




if not bProcessed:
	ap.showHelp()
















