

import datetime
import pytz

from jk_cachefunccalls import cacheCalls

from .parsing_utils import *
from .invoke_utils import run



#
#
#
def parse_date_as_datetime(stdout:str, stderr:str, exitcode:int, utc:bool = False) -> datetime.datetime:

	"""
	2019-09-01-23-03-53-549067419
	"""

	if exitcode != 0:
		raise Exception()

	sYear, sMonth, sDay, sHours, sMinutes, sSeconds, sNanoSeconds = stdout.strip().split("-")

	if utc:
		return datetime.datetime(
			int(sYear), int(sMonth), int(sDay), int(sHours), int (sMinutes), int(sSeconds), int(sNanoSeconds)//1000,
			pytz.UTC)
	else:
		return datetime.datetime(
			int(sYear), int(sMonth), int(sDay), int(sHours), int (sMinutes), int(sSeconds), int(sNanoSeconds)//1000)
#



#
# Get the date as reported by the (possibly remote) operating system.
#
def get_date(c = None, utc:bool = True) -> dict:
	# NOTE: some systems will always return UTC.
	# we need a way to identify if UTC is returned or not.
	stdout, stderr, exitcode = run(c, "/bin/date " + ("-u" if utc else "") + " +'%Y-%m-%d-%H-%M-%S-%N'")
	d = parse_date_as_datetime(stdout, stderr, exitcode, utc)
	return {
		"year": d.year,
		"month": d.month,
		"day": d.day,
		"hour": d.hour,
		"minute": d.minute,
		"second": d.second,
		"millisecond": d.microsecond // 1000,
	}
#



#
# Get the date as reported by the (possibly remote) operating system.
#
def get_date_as_datetime(c = None, utc:bool = True) -> datetime.datetime:
	stdout, stderr, exitcode = run(c, "/bin/date " + ("-u" if utc else "") + " +'%Y-%m-%d-%H-%M-%S-%N'")
	return parse_date_as_datetime(stdout, stderr, exitcode, utc)
#















