#!/usr/bin/python3



import jk_sysinfo

import jk_json



#jk_sysinfo.enableDebugging()

result = jk_sysinfo.get_proc_load_avg()
print()
jk_json.prettyPrint(result)
print()


