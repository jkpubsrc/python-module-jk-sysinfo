#!/usr/bin/python3


import time

import jk_sysinfo

import jk_json



#jk_sysinfo.enableDebugging()

t0 = time.time()
result = jk_sysinfo.get_ps_local()
t1 = time.time()
print(t1 - t0)

print()
jk_json.prettyPrint(result)
print()


