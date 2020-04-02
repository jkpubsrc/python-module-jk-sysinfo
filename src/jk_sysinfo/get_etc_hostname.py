

import os

from jk_cachefunccalls import cacheCalls
import jk_etcpasswd

from .parsing_utils import *
from .invoke_utils import run





def parse_etc_hostname(stdout:str) -> dict:
	return {
		"hostname": stdout.strip()
	}
#



def get_etc_hostname(c = None) -> dict:
	stdout, stderr, exitcode = run(c, "cat /etc/hostname")

	return parse_etc_hostname(stdout)
#















