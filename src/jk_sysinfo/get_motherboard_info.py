

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
	vendor, _, _ = run(c, "cat /sys/devices/virtual/dmi/id/board_vendor")
	name, _, _ = run(c, "cat /sys/devices/virtual/dmi/id/board_name")
	version, _, _ = run(c, "cat /sys/devices/virtual/dmi/id/board_version")

	return {
		"vendor": vendor.strip(),
		"name": name.strip(),
		"version": version.strip(),
	}
#







