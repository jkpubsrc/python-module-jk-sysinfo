#!/usr/bin/python3



import jk_sysinfo

import jk_json



#jk_sysinfo.enableDebugging()

result = jk_sysinfo.get_lshw()
print()
jk_json.saveToFilePretty(result, "test_get_lshw.json")
print()


