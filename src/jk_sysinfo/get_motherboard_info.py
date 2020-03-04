

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
def get_motherboard_info(c = None) -> dict:
	bFail = False

	try:
		model, _, _ = run(c, "cat /sys/firmware/devicetree/base/model")
		PATTERN = "Raspberry Pi"
		if model.startswith(PATTERN):
			return {
				"vendor": "Raspberry Pi Foundation",
				"name": "Raspberry Pi",
				"version": model[len(PATTERN):].strip(),
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
				"vendor": vendor.strip(),
				"name": name.strip(),
				"version": version.strip(),
			}
		except:
			bFail = True

	if bFail:
		return {}
		#raise Exception("Unknown system layout: Can't retrieve required information!")
#







