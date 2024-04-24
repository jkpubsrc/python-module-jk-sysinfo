#!/usr/bin/python3



import jk_sysinfo

import jk_json



#jk_sysinfo.enableDebugging()

print()
print("#" * 120)
print()

result = jk_sysinfo.get_vcgencmd_get_config()
print()
jk_json.prettyPrint(result)
print()

result = jk_sysinfo.get_vcgencmd_measure_volts()
print()
jk_json.prettyPrint(result)
print()

result = jk_sysinfo.get_vcgencmd_measure_temp()
print()
jk_json.prettyPrint(result)
print()

result = jk_sysinfo.get_vcgencmd_get_mem()
print()
jk_json.prettyPrint(result)
print()

result = jk_sysinfo.get_vcgencmd_display_power()
print()
jk_json.prettyPrint(result)
print()



print("#" * 120)



result = jk_sysinfo.get_vcgencmd()
print()
jk_json.prettyPrint(result)

print()
print("#" * 120)
print()









