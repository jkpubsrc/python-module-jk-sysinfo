

from jk_cachefunccalls import cacheCalls

from .parsing_utils import *
from .invoke_utils import run






#
# Note: This function does not work on Raspberry Pi computers.
#
# Returns:
#	{
#		"date": "12/06/2017",
#		"vendor": "American Megatrends Inc.",
#		"version": "1.A0"
#	}
#
@cacheCalls(seconds=3, dependArgs=[0])
def get_bios_info(c = None) -> dict:
	bFail = False

	try:
		date, _, _ = run(c, "cat /sys/devices/virtual/dmi/id/bios_date")
		vendor, _, _ = run(c, "cat /sys/devices/virtual/dmi/id/bios_vendor")
		version, _, _ = run(c, "cat /sys/devices/virtual/dmi/id/bios_version")

		return {
			"date": date.strip(),
			"vendor": vendor.strip(),
			"version": version.strip(),
		}
	except:
		bFail = True

	if bFail:
		return {}
		#raise Exception("Unknown system layout: Can't retrieve required information!")
#







