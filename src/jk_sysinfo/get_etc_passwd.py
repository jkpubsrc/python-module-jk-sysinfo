

import os

from jk_cachefunccalls import cacheCalls
import jk_etcpasswd

from .parsing_utils import *
from .invoke_utils import run





def parse_etc_passwd(stdoutPasswd:str, stdoutShadow:str) -> dict:
	pwdFile = jk_etcpasswd.PwdFile("/etc/passwd", "/etc/shadow", stdoutPasswd, stdoutShadow)
	return pwdFile.toJSON()
#



def get_etc_passwd(c = None) -> dict:
	if os.geteuid() != 0:
		raise Exception("Must be root!")

	stdoutPasswd, stderrPasswd, exitcodePasswd = run(c, "cat /etc/passwd")
	assert exitcodePasswd == 0
	assert not stderrPasswd

	stdoutShadow, stderrShadow, exitcodeShadow = run(c, "cat /etc/shadow")
	assert exitcodeShadow == 0
	assert not stderrShadow

	return parse_etc_passwd(stdoutPasswd, stdoutShadow)
#















