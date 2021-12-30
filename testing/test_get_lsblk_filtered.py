#!/usr/bin/python3



import jk_sysinfo

import jk_json



#jk_sysinfo.enableDebugging()

result = jk_sysinfo.get_lsblk()
result = jk_sysinfo.filter_lsblk_devtree(result, type="disk")
print()
jk_json.prettyPrint(result)
print()


