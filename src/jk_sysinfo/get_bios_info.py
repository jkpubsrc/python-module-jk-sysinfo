

from .parsing_utils import *
from .invoke_utils import run






#
# Returns:
#	{
#		"date": "12/06/2017",
#		"vendor": "American Megatrends Inc.",
#		"version": "1.A0"
#	}
#
def get_bios_info(c = None) -> dict:
	date, _, _ = run(c, "cat /sys/devices/virtual/dmi/id/bios_date")
	vendor, _, _ = run(c, "cat /sys/devices/virtual/dmi/id/bios_vendor")
	version, _, _ = run(c, "cat /sys/devices/virtual/dmi/id/bios_version")

	return {
		"date": date.strip(),
		"vendor": vendor.strip(),
		"version": version.strip(),
	}
#







