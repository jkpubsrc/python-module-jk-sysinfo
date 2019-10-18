#!/usr/bin/python3


import os
import sys
import re
import time
import json

import jk_sysinfo
#import jk_json
#import jk_flexdata
import jk_utils








from fabric import Connection
import jk_pwdinput

#REMOTE_HOST = "192.168.11.36"
REMOTE_HOST = "127.0.0.1"
REMOTE_PORT = 22
#REMOTE_LOGIN = "jknauth"
REMOTE_LOGIN = "woodoo"
REMOTE_PASSWORD = jk_pwdinput.readpwd("Password for " + REMOTE_LOGIN + "@" + REMOTE_HOST + ": ")
c = Connection(host=REMOTE_HOST, user=REMOTE_LOGIN, port=REMOTE_PORT, connect_kwargs={"password": REMOTE_PASSWORD})

SYSTEM_ID = "selenium"
#SYSTEM_ID = "nbjk"

#PRETTY = False
PRETTY = True

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






print("Now repeatedly retrieving data ...")

while True:
	data = {}
	tAll = time.time()
	for key, retriever in RETRIEVERS:
		t = time.time()
		try:
			v = retriever(c)
		except Exception as ee:
			print("ERROR @ " + key)
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
	print("Duration:", dtAll)

	if PRETTY:
		s = json.dumps(data, indent="\t")
	else:
		s = json.dumps(data)

	with jk_utils.file_rw.openWriteText("data/" + SYSTEM_ID + ".json", bSafeWrite=True) as f:
		f.write(s)

	time.sleep(10)





















