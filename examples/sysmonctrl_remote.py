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

stdout, stderr, exitcode = jk_sysinfo.run(c, "/home/woodoo/DevOS/PythonModules/jk_sysinfo/examples/sysmonctrl.py sysinfo")
if exitcode != 0:
	print("FAILED!")
else:
	with open("sysmonctrl.json", "w") as f:
		f.write(stdout)
	print(stderr)

