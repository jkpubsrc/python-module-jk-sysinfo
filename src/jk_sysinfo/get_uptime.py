

import datetime
import pytz
from dateutil import tz

from jk_cachefunccalls import cacheCalls

from .parsing_utils import *
from .invoke_utils import run
from .get_date import *



_EPOCH = datetime.datetime(1970, 1, 1, 0, 0, 0, 0, pytz.UTC)




#
#
#
def parse_uptime(stdout:str, stderr:str, exitcode:int) -> float:

	"""
	395207.66 1784474.45
	"""

	if exitcode != 0:
		raise Exception()

	sUptime, _ = stdout.strip().split(" ")
	uptimeInSeconds = float(sUptime)

	return uptimeInSeconds
#



#
# Returns:
#
#	{
#		"systemNow": 1567404690.778003,
#		"systemNowLocal": {
#				"day": 2,
#				"hour": 9,
#				"millisecond": 778,
#				"minute": 11,
#				"month": 9,
#				"second": 30,
#				"year": 2019
#		},
#		"systemNowUTC": {
#				"day": 2,
#				"hour": 6,
#				"millisecond": 778,
#				"minute": 11,
#				"month": 9,
#				"second": 30,
#				"year": 2019
#		},
#		"systemStartTime": 1566972543.348003,
#		"systemStartTimeLocal": {
#				"day": 28,
#				"hour": 9,
#				"millisecond": 348,
#				"minute": 9,
#				"month": 8,
#				"second": 3,
#				"year": 2019
#		},
#		"systemStartTimeUTC": {
#				"day": 28,
#				"hour": 6,
#				"millisecond": 348,
#				"minute": 9,
#				"month": 8,
#				"second": 3,
#				"year": 2019
#		},
#		"uptimeInSeconds": 432147.43
#	}
#
def get_uptime(c = None) -> dict:
	systemNowInDateTimeUTC = get_date_as_datetime(None, True)
	systemNowInSeconds = (systemNowInDateTimeUTC - _EPOCH).total_seconds()
	systemNowInDateTimeLocal = systemNowInDateTimeUTC.astimezone(tz.tzlocal())

	stdout, stderr, exitcode = run(c, "cat /proc/uptime")
	uptimeInSeconds = parse_uptime(stdout, stderr, exitcode)

	systemStartInSeconds = systemNowInSeconds - uptimeInSeconds
	systemStartInDateTimeUTC = datetime.datetime.utcfromtimestamp(systemStartInSeconds).replace(tzinfo=pytz.UTC)
	systemStartInDateTimeLocal = systemStartInDateTimeUTC.astimezone(tz.tzlocal())

	ret = {
		"systemNow": systemNowInSeconds,
		"systemNowUTC": {
			"year": systemNowInDateTimeUTC.year,
			"month": systemNowInDateTimeUTC.month,
			"day": systemNowInDateTimeUTC.day,
			"hour": systemNowInDateTimeUTC.hour,
			"minute": systemNowInDateTimeUTC.minute,
			"second": systemNowInDateTimeUTC.second,
			"millisecond": systemNowInDateTimeUTC.microsecond // 1000,
		},
		"systemNowLocal": {
			"year": systemNowInDateTimeLocal.year,
			"month": systemNowInDateTimeLocal.month,
			"day": systemNowInDateTimeLocal.day,
			"hour": systemNowInDateTimeLocal.hour,
			"minute": systemNowInDateTimeLocal.minute,
			"second": systemNowInDateTimeLocal.second,
			"millisecond": systemNowInDateTimeLocal.microsecond // 1000,
		},
		"systemStartTime": systemStartInSeconds,
		"systemStartTimeUTC": {
			"year": systemStartInDateTimeUTC.year,
			"month": systemStartInDateTimeUTC.month,
			"day": systemStartInDateTimeUTC.day,
			"hour": systemStartInDateTimeUTC.hour,
			"minute": systemStartInDateTimeUTC.minute,
			"second": systemStartInDateTimeUTC.second,
			"millisecond": systemStartInDateTimeUTC.microsecond // 1000,
		},
		"systemStartTimeLocal": {
			"year": systemStartInDateTimeLocal.year,
			"month": systemStartInDateTimeLocal.month,
			"day": systemStartInDateTimeLocal.day,
			"hour": systemStartInDateTimeLocal.hour,
			"minute": systemStartInDateTimeLocal.minute,
			"second": systemStartInDateTimeLocal.second,
			"millisecond": systemStartInDateTimeLocal.microsecond // 1000,
		},
		"uptimeInSeconds": uptimeInSeconds,
	}

	return ret
#















