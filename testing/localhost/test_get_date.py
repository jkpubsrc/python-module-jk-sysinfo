#!/usr/bin/python3



import jk_sysinfo

import jk_json



#jk_sysinfo.enableDebugging()

print(jk_sysinfo.get_date_as_datetime())
print()
result = jk_sysinfo.get_date()
jk_json.prettyPrint(result)
print()






