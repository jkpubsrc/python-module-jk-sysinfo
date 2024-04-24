#!/usr/bin/python3



import jk_sysinfo

import jk_json



#jk_sysinfo.enableDebugging()

for i in range(0, 256):
	print(i)
	result = jk_sysinfo.get_dmi_decode(typeNo=i)
print()



print()
print()
print()
result = jk_sysinfo.get_dmi_decode(typeNo=2)
jk_json.prettyPrint(result)
print()


