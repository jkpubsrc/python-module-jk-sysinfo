

from jk_cachefunccalls import cacheCalls

from .parsing_utils import *
from .invoke_utils import run



#
# Returns:
#
#	{
#		"sirius": {
#			"user": "sirius",
#			"userID": 1000,
#			"groupID": 1000,
#			"homeDir": "/home/sirius",
#			"shell": "/bin/bash"
#		},
#		...
#	}
#
def parse_user_info_etc_passwd(stdout:str, stderr:str, exitcode:int) -> dict:

	"""
	root:x:0:0:root:/root:/bin/bash
	daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
	bin:x:2:2:bin:/bin:/usr/sbin/nologin
	sys:x:3:3:sys:/dev:/usr/sbin/nologin
	sync:x:4:65534:sync:/bin:/bin/sync
	games:x:5:60:games:/usr/games:/usr/sbin/nologin
	man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
	lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
	mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
	news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
	uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
	proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
	www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
	backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
	list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
	irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
	gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
	nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
	systemd-network:x:100:102:systemd Network Management,,,:/run/systemd/netif:/usr/sbin/nologin
	systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd/resolve:/usr/sbin/nologin
	syslog:x:102:106::/home/syslog:/usr/sbin/nologin
	messagebus:x:103:107::/nonexistent:/usr/sbin/nologin
	_apt:x:104:65534::/nonexistent:/usr/sbin/nologin
	uuidd:x:105:111::/run/uuidd:/usr/sbin/nologin
	avahi-autoipd:x:106:112:Avahi autoip daemon,,,:/var/lib/avahi-autoipd:/usr/sbin/nologin
	usbmux:x:107:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
	dnsmasq:x:108:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
	rtkit:x:109:114:RealtimeKit,,,:/proc:/usr/sbin/nologin
	speech-dispatcher:x:110:29:Speech Dispatcher,,,:/var/run/speech-dispatcher:/bin/false
	whoopsie:x:111:117::/nonexistent:/bin/false
	kernoops:x:112:65534:Kernel Oops Tracking Daemon,,,:/:/usr/sbin/nologin
	saned:x:113:119::/var/lib/saned:/usr/sbin/nologin
	pulse:x:114:120:PulseAudio daemon,,,:/var/run/pulse:/usr/sbin/nologin
	avahi:x:115:122:Avahi mDNS daemon,,,:/var/run/avahi-daemon:/usr/sbin/nologin
	colord:x:116:123:colord colour management daemon,,,:/var/lib/colord:/usr/sbin/nologin
	hplip:x:117:7:HPLIP system user,,,:/var/run/hplip:/bin/false
	geoclue:x:118:124::/var/lib/geoclue:/usr/sbin/nologin
	gnome-initial-setup:x:119:65534::/run/gnome-initial-setup/:/bin/false
	gdm:x:120:125:Gnome Display Manager:/var/lib/gdm3:/bin/false
	sirius:x:1000:1000::/home/sirius:/bin/bash
	cups-pk-helper:x:121:116:user for cups-pk-helper service,,,:/home/cups-pk-helper:/usr/sbin/nologin
	festival:x:122:29::/nonexistent:/usr/sbin/nologin
	timidity:x:123:128:TiMidity++ MIDI sequencer service:/etc/timidity:/usr/sbin/nologin
	sddm:x:124:129:Simple Desktop Display Manager:/var/lib/sddm:/bin/false
	statd:x:125:65534::/var/lib/nfs:/usr/sbin/nologin
	sshd:x:126:65534::/run/sshd:/usr/sbin/nologin
	"""

	if exitcode != 0:
		raise Exception()

	lines = stdout.strip().split("\n")

	ret = {}
	for line in lines:
		userName, x, sUserID, sGroupID, comment, homeDir, shell = line.split(":")
		ret[userName] = {
			"user": userName,
			"userID": int(sUserID),
			"groupID": int(sGroupID),
			"homeDir": None if homeDir == "/nonexistent" else homeDir,
			"shell": None if shell == "/usr/sbin/nologin" else shell,
		}

	return ret
#



#
# Returns:
#
#	{
#		"sirius": {
#			"user": "sirius",
#			"isLocked": False,
#			"hasPassword": True
#		},
#		...
#	}
#
def parse_user_info_etc_shadow(stdout:str, stderr:str, exitcode:int) -> dict:

	"""
	root:$6$iSgU4RbH$....:17970:0:99999:7:::
	daemon:*:17647:0:99999:7:::
	bin:*:17647:0:99999:7:::
	sys:*:17647:0:99999:7:::
	sync:*:17647:0:99999:7:::
	games:*:17647:0:99999:7:::
	man:*:17647:0:99999:7:::
	lp:*:17647:0:99999:7:::
	mail:*:17647:0:99999:7:::
	news:*:17647:0:99999:7:::
	uucp:*:17647:0:99999:7:::
	proxy:*:17647:0:99999:7:::
	www-data:*:17647:0:99999:7:::
	backup:*:17647:0:99999:7:::
	list:*:17647:0:99999:7:::
	irc:*:17647:0:99999:7:::
	gnats:*:17647:0:99999:7:::
	nobody:*:17647:0:99999:7:::
	systemd-network:*:17647:0:99999:7:::
	systemd-resolve:*:17647:0:99999:7:::
	syslog:*:17647:0:99999:7:::
	messagebus:*:17647:0:99999:7:::
	_apt:*:17647:0:99999:7:::
	uuidd:*:17647:0:99999:7:::
	avahi-autoipd:*:17647:0:99999:7:::
	usbmux:*:17647:0:99999:7:::
	dnsmasq:*:17647:0:99999:7:::
	rtkit:*:17647:0:99999:7:::
	speech-dispatcher:!:17647:0:99999:7:::
	whoopsie:*:17647:0:99999:7:::
	kernoops:*:17647:0:99999:7:::
	saned:*:17647:0:99999:7:::
	pulse:*:17647:0:99999:7:::
	avahi:*:17647:0:99999:7:::
	colord:*:17647:0:99999:7:::
	hplip:*:17647:0:99999:7:::
	geoclue:*:17647:0:99999:7:::
	gnome-initial-setup:*:17647:0:99999:7:::
	gdm:*:17647:0:99999:7:::
	sirius:$6$Bf.KreAS$....:18136:0:99999:7:::
	cups-pk-helper:*:17970:0:99999:7:::
	festival:*:17977:0:99999:7:::
	timidity:*:17977:0:99999:7:::
	sddm:*:17977:0:99999:7:::
	statd:*:17977:0:99999:7:::
	sshd:*:17977:0:99999:7:::
	"""

	if exitcode != 0:
		raise Exception()

	lines = stdout.strip().split("\n")

	ret = {}
	for line in lines:
		userName, password, x1, x2, x3, x4, x5, x6, x7 = line.split(":")
		x = {
			"user": userName,
			"isDisabled": password.startswith("!"),
			"hasPassword": (password.startswith("$") or password.startswith("!$")) and (len(password) > 10),
		}
		x["canLogin"] = x["hasPassword"] and not x["isDisabled"]
		ret[userName] = x

	return ret
#



#
# Returns:
#
#	{
#		"sirius": {
#			"group": "sirius",
#			"groupID": 1000,
#			"usersInGroup": []
#		},
#		...
#	}
#
def parse_user_info_etc_group(stdout:str, stderr:str, exitcode:int) -> dict:

	"""
	root:x:0:
	daemon:x:1:
	bin:x:2:
	sys:x:3:
	adm:x:4:syslog,sirius
	tty:x:5:
	disk:x:6:
	lp:x:7:
	mail:x:8:
	news:x:9:
	uucp:x:10:
	man:x:12:
	proxy:x:13:
	kmem:x:15:
	dialout:x:20:
	fax:x:21:
	voice:x:22:
	cdrom:x:24:sirius
	floppy:x:25:
	tape:x:26:
	sudo:x:27:sirius
	audio:x:29:pulse,timidity
	dip:x:30:sirius
	www-data:x:33:
	backup:x:34:
	operator:x:37:
	list:x:38:
	irc:x:39:
	src:x:40:
	gnats:x:41:
	shadow:x:42:
	utmp:x:43:
	video:x:44:
	sasl:x:45:
	plugdev:x:46:sirius
	staff:x:50:
	games:x:60:
	users:x:100:
	nogroup:x:65534:
	systemd-journal:x:101:
	systemd-network:x:102:
	systemd-resolve:x:103:
	input:x:104:
	crontab:x:105:
	syslog:x:106:
	messagebus:x:107:
	netdev:x:108:
	mlocate:x:109:
	ssl-cert:x:110:
	uuidd:x:111:
	avahi-autoipd:x:112:
	bluetooth:x:113:
	rtkit:x:114:
	ssh:x:115:
	lpadmin:x:116:sirius
	whoopsie:x:117:
	scanner:x:118:saned
	saned:x:119:
	pulse:x:120:
	pulse-access:x:121:
	avahi:x:122:
	colord:x:123:
	geoclue:x:124:
	gdm:x:125:
	sirius:x:1000:
	sambashare:x:126:sirius
	_cvsadmin:x:127:
	timidity:x:128:
	sddm:x:129:
	"""

	if exitcode != 0:
		raise Exception()

	lines = stdout.strip().split("\n")

	ret = {}
	for line in lines:
		groupName, x, sGroupID, usersInGroup = line.split(":")
		ret[groupName] = {
			"group": groupName,
			"groupID": int(sGroupID),
			"usersInGroup": [] if not usersInGroup else usersInGroup.split(","),
		}

	return ret
#



#
# Returns:
#
#	{
#		"sirius": {
#				"groupID": 1000,
#				"groups": [
#						"adm",
#						"cdrom",
#						"sudo",
#						"dip",
#						"plugdev",
#						"lpadmin",
#						"sambashare"
#				],
#				"hasPassword": true,
#				"homeDir": "/home/sirius",
#				"isLocked": false,
#				"shell": "/bin/bash",
#				"user": "sirius",
#				"userID": 1000
#		},
#		...
#	}
#
@cacheCalls(seconds=3, dependArgs=[0])
def get_user_info(c = None, catEtcShadowScriptCmd:str = None) -> dict:
	if catEtcShadowScriptCmd is None:
		catEtcShadowScriptCmd = "cat /etc/shadow"

	stdOutPasswd, stdErrPasswd, exitCodePasswd = run(c, "cat /etc/passwd")
	stdOutShadow, stdErrShadow, exitCodeShadow = run(c, "sudo " + catEtcShadowScriptCmd)

	retUsers = joinDictsByKey(
		parse_user_info_etc_passwd(stdOutPasswd, stdErrPasswd, exitCodePasswd),
		parse_user_info_etc_shadow(stdOutShadow, stdErrShadow, exitCodeShadow),
	)

	stdOutGroup, stdErrGroup, exitCodeGroup = run(c, "cat /etc/group")
	groups = parse_user_info_etc_group(stdOutGroup, stdErrGroup, exitCodeGroup)

	for data in retUsers.values():
		data["groups"] = []

	for data in groups.values():
		for user in data["usersInGroup"]:
			retUsers[user]["groups"].append(data["group"])

	return retUsers
#















