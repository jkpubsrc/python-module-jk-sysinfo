#!/usr/bin/python3



import jk_sysinfo

import jk_json



#jk_sysinfo.enableDebugging()

result = jk_sysinfo.get_docker_stats()
print()
jk_json.prettyPrint(result)
print()


