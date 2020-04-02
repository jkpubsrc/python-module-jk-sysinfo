

import os

from jk_cachefunccalls import cacheCalls
import jk_etcpasswd

from .parsing_utils import *
from .invoke_utils import run





def parse_etc_group(stdoutGroup:str, stdoutGShadow:str) -> dict:
	grpFile = jk_etcpasswd.GrpFile("/etc/group", "/etc/gshadow", stdoutGroup, stdoutGShadow)
	return grpFile.toJSON()
#



def get_etc_group(c = None) -> dict:
	if os.geteuid() != 0:
		raise Exception("Must be root!")

	stdoutGroup, stderrGroup, exitcodeGroup = run(c, "cat /etc/group")
	assert exitcodeGroup == 0
	assert not stderrGroup

	stdoutGShadow, stderrGShadow, exitcodeGShadow = run(c, "cat /etc/gshadow")
	assert exitcodeGShadow == 0
	assert not stderrGShadow

	return parse_etc_group(stdoutGroup, stdoutGShadow)
#















