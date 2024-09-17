

from jk_cachefunccalls import cacheCalls

from .parsing_utils import *
from .invoke_utils import run






#
# Returns:
#	{
#		"name": "B150M ECO (MS-7994)",
#		"vendor": "MSI",
#		"version": "1.0"
#	}
#
@cacheCalls(seconds=3, dependArgs=[0])
def get_motherboard_info(c = None) -> dict:
	bFail = False

	try:
		# TODO: sysinfo.py avoids calling this method on Raspberry Pi devices thus working around getting the desired information this way. 
		model, _, _ = run(c, "cat /sys/firmware/devicetree/base/model")
		PATTERN = "Raspberry Pi"
		if model.startswith(PATTERN):
			return {
				"vendor": "Raspberry Pi Foundation",
				"name": "Raspberry Pi",
				"version": model[len(PATTERN):].strip().strip("\u0000"),
			}
		else:
			print(repr(model))
			bFail = True
	except:
		try:
			vendor, _, _ = run(c, "cat /sys/devices/virtual/dmi/id/board_vendor")
			name, _, _ = run(c, "cat /sys/devices/virtual/dmi/id/board_name")
			version, _, _ = run(c, "cat /sys/devices/virtual/dmi/id/board_version")

			return {
				"vendor": vendor.strip().strip("\u0000"),
				"name": name.strip().strip("\u0000"),
				"version": version.strip().strip("\u0000"),
			}
		except:
			bFail = True

	if bFail:
		return {}
		#raise Exception("Unknown system layout: Can't retrieve required information!")
#







