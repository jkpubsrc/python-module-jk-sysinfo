

import re
import pwd

from .parsing_utils import *
from .invoke_utils import run



_parserColonKVP = ParseAtFirstDelimiter(delimiter="=", valueCanBeWrappedInDoubleQuotes=True)



#
# Returns:
#
#	[
#			{
#					"args": "splash",
#					"cmd": "/sbin/init",
#					"pid": 1,
#					"ppid": 0,
#					"stat": "Ss",
#					"time": "0:04",
#					"tty": null,
#					"uid": 0,
#					"user": "root"
#			},
#			{
#					"cmd": "[kthreadd]",
#					"pid": 2,
#					"ppid": 0,
#					"stat": "S",
#					"time": "0:00",
#					"tty": null,
#					"uid": 0,
#					"user": "root"
#			},
#			{
#					"cmd": "[ksoftirqd/0]",
#					"pid": 3,
#					"ppid": 2,
#					"stat": "S",
#					"time": "0:02",
#					"tty": null,
#					"uid": 0,
#					"user": "root"
#			},
#			...
#			{
#					"cmd": "bash",
#					"pid": 20144,
#					"ppid": 14839,
#					"stat": "Ss+",
#					"time": "0:00",
#					"tty": "pts/3",
#					"uid": 1000,
#					"user": "woodoo"
#			},
#			{
#					"args": "--spawner :1.9 /org/gtk/gvfs/exec_spaw/4",
#					"cmd": "/usr/lib/gvfs/gvfsd-computer",
#					"pid": 20292,
#					"ppid": 1,
#					"stat": "Sl",
#					"time": "0:00",
#					"tty": null,
#					"uid": 1000,
#					"user": "woodoo"
#			},
#			...
#			{
#					"args": "/usr/share/code/resources/app/extensions/json-language-features/server/dist/jsonServerMain --node-ipc --clientProcessId=15491",
#					"cmd": "/usr/share/code/code",
#					"pid": 29554,
#					"ppid": 15491,
#					"stat": "Sl",
#					"time": "0:05",
#					"tty": null,
#					"uid": 1000,
#					"user": "woodoo"
#			},
#			{
#					"args": "--spawner :1.9 /org/gtk/gvfs/exec_spaw/6",
#					"cmd": "/usr/lib/gvfs/gvfsd-mtp",
#					"pid": 31616,
#					"ppid": 1,
#					"stat": "Sl",
#					"time": "0:25",
#					"tty": null,
#					"uid": 1000,
#					"user": "woodoo"
#			}
#	]
#
def parse_ps(stdout:str, stderr:str, exitcode:int) -> dict:

	"""
	 PPID   PID  PGID   SID TTY      TPGID STAT   UID   TIME COMMAND
		0     1     1     1 ?           -1 Ss       0   0:04 /sbin/init splash
		0     2     0     0 ?           -1 S        0   0:00 [kthreadd]
		2     3     0     0 ?           -1 S        0   0:02 [ksoftirqd/0]
		2     5     0     0 ?           -1 S<       0   0:00 [kworker/0:0H]
		2     7     0     0 ?           -1 S        0   4:44 [rcu_sched]
		2     8     0     0 ?           -1 S        0   0:00 [rcu_bh]
		2     9     0     0 ?           -1 S        0   0:00 [migration/0]
		2    10     0     0 ?           -1 S        0   0:01 [watchdog/0]
		2    11     0     0 ?           -1 S        0   0:01 [watchdog/1]
		2    12     0     0 ?           -1 S        0   0:00 [migration/1]
	...
		1   270   270   270 ?           -1 Ss       0   0:26 /lib/systemd/systemd-journald
		2   273     0     0 ?           -1 S        0   0:00 [kauditd]
		2   323     0     0 ?           -1 S<       0   0:00 [rpciod]
		1   360   360   360 ?           -1 Ss       0   0:00 /lib/systemd/systemd-udevd
		2   532     0     0 ?           -1 S<       0   0:00 [kvm-irqfd-clean]
		2   537     0     0 ?           -1 S<       0   0:00 [kworker/1:1H]
		2   558     0     0 ?           -1 S        0   0:00 [irq/124-mei_me]
		2   578     0     0 ?           -1 S<       0   0:00 [kworker/3:1H]
		1   605   605   605 ?           -1 Ssl      0   0:00 /usr/sbin/ModemManager
		1   609   609   609 ?           -1 Ss       0   0:01 /usr/sbin/cron -f
		1   610   610   610 ?           -1 Ss       0   6:45 /usr/sbin/acpid
		1   639   639   639 ?           -1 Ss       0   0:00 /lib/systemd/systemd-logind
		1   651   651   651 ?           -1 Ss       0   0:00 /usr/sbin/smartd -n
		1   660   660   660 ?           -1 Ss       0   0:00 /usr/sbin/avahi-dnsconfd -s
		1   662   662   662 ?           -1 Ss       1   0:00 /usr/sbin/atd -f
		1   669   669   669 ?           -1 Ssl      0   0:10 /usr/lib/accountsservice/accounts-daemon
		1   670   670   670 ?           -1 Ss     112   0:01 avahi-daemon: running [selenium.local]
		1   675   675   675 ?           -1 Ss     106   0:02 /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation
	  670   727   670   670 ?           -1 S      112   0:00 avahi-daemon: chroot helper
		1   792   792   792 ?           -1 Ssl      0   0:00 /usr/sbin/NetworkManager --no-daemon
		1   793   793   793 ?           -1 Ssl    104   0:08 /usr/sbin/rsyslogd -n
		2   827     0     0 ?           -1 S<       0   0:12 [kworker/2:1H]
		1   877   876   876 ?           -1 Sl      33   0:00 /usr/bin/mono /usr/lib/mono/4.5/xsp4.exe --port 8084 --address 0.0.0.0 --appconfigdir /etc/xsp4 --nonstop
		1   879   879   879 ?           -1 Ss       0   0:31 /usr/sbin/irqbalance --pid=/var/run/irqbalance.pid
		1   881   881   881 ?           -1 Ssl      0   0:00 /usr/lib/policykit-1/polkitd --no-debug
		1   895   895   895 ?           -1 SLsl     0   0:00 /usr/sbin/lightdm
		1   952   952   952 ?           -1 Ssl    113   0:00 /usr/lib/colord/colord
		1   984   983   983 ?           -1 S      128   0:14 /usr/bin/uml_switch -unix /var/run/uml-utilities/uml_switch.ctl
	  895  1054  1054  1054 tty7      1054 Ssl+     0 500:33 /usr/lib/xorg/Xorg -core :0 -seat seat0 -auth /var/run/lightdm/root/:0 -nolisten tcp vt7 -novtswitch
	  895  1139   895   895 ?           -1 Sl       0   0:00 lightdm --session-child 12 19
		1  1743  1743  1743 ?           -1 Ssl    131   0:25 /usr/bin/memcached -m 64 -p 11211 -u memcache -l 127.0.0.1
		1  1749  1749  1749 ?           -1 Ssl      0   0:00 /usr/bin/python3 /usr/share/unattended-upgrades/unattended-upgrade-shutdown --wait-for-signal
		1  1754  1754  1754 ?           -1 Ssl    110   0:00 /usr/bin/whoopsie -f
		1  1772  1772  1772 ?           -1 Ssl      0  12:11 /usr/bin/containerd
		1  1787  1787  1787 ?           -1 Ssl    125   6:59 /usr/sbin/mysqld
	...
	15470 15491  3035  3035 ?           -1 Sl    1000   4:30 /usr/share/code/code --nolazy --inspect=22119 /usr/share/code/resources/app/out/bootstrap-fork --type=extensionHost
	15470 15492  3035  3035 ?           -1 Sl    1000   0:17 /usr/share/code/code /usr/share/code/resources/app/out/bootstrap-fork --type=watcherService
	15491 15592  3035  3035 ?           -1 SLl   1000  90:06 /home/woodoo/.vscode/extensions/ms-python.python-2019.10.41019/languageServer.0.4.58/Microsoft.Python.LanguageServer
		2 15839     0     0 ?           -1 S        0   0:00 [kworker/u8:0]
	14633 15864  3035  3035 ?           -1 Sl    1000   8:19 /usr/share/code/code --type=renderer --disable-color-correct-rendering --no-sandbox --enable-features=SharedArrayBuffer --disable-features=SpareRendererForSitePerProcess --service-pipe-token=15711160101535984269 --lang=en-US --app-path=/usr/share/code/resources/app --user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Code/1.37.0 Chrome/69.0.3497.128 Electron/4.2.7 Safari/537.36 --node-integration=true --webview-tag=true --no-sandbox --background-color=#1e1e1e --num-raster-threads=2 --enable-main-frame-before-activation --service-request-channel-token=15711160101535984269 --renderer-client-id=9 --shared-files=v8_context_snapshot_data:100,v8_natives_data:101
	...
	"""

	if exitcode != 0:
		raise Exception()

	lines = stdout.strip().split("\n")
	lines2 = splitAtVerticalSpaceColumnsFirstLineIsHeader(lines)

	#	0		1	2		3	4		5		6	7		8	9
	#  PPID   PID  PGID   SID TTY      TPGID STAT   UID   TIME COMMAND

	ret = []
	for group in lines2:
		uid = int(group[7])
		data = {
			"ppid": int(group[0]),
			"pid": int(group[1]),
			"tty": None if group[4] == "?" else group[4],
			"stat": group[6],
			"uid": uid,
			"time": group[8],
		}
		pos = group[9].find(" ")
		if pos > 0:
			data["cmd"] = group[9][:pos]
			data["args"] = group[9][pos+1:]
		else:
			data["cmd"] = group[9]

		pwdEntry = pwd.getpwuid(uid)
		if pwdEntry:
			data["user"] = pwdEntry.pw_name

		ret.append(data)

	return ret
#



#
# Returns:
#
#	[
#			{
#					"args": "splash",
#					"cmd": "/sbin/init",
#					"pid": 1,
#					"ppid": 0,
#					"stat": "Ss",
#					"time": "0:04",
#					"tty": null,
#					"uid": 0,
#					"user": "root"
#			},
#			{
#					"cmd": "[kthreadd]",
#					"pid": 2,
#					"ppid": 0,
#					"stat": "S",
#					"time": "0:00",
#					"tty": null,
#					"uid": 0,
#					"user": "root"
#			},
#			{
#					"cmd": "[ksoftirqd/0]",
#					"pid": 3,
#					"ppid": 2,
#					"stat": "S",
#					"time": "0:02",
#					"tty": null,
#					"uid": 0,
#					"user": "root"
#			},
#			...
#			{
#					"cmd": "bash",
#					"pid": 20144,
#					"ppid": 14839,
#					"stat": "Ss+",
#					"time": "0:00",
#					"tty": "pts/3",
#					"uid": 1000,
#					"user": "woodoo"
#			},
#			{
#					"args": "--spawner :1.9 /org/gtk/gvfs/exec_spaw/4",
#					"cmd": "/usr/lib/gvfs/gvfsd-computer",
#					"pid": 20292,
#					"ppid": 1,
#					"stat": "Sl",
#					"time": "0:00",
#					"tty": null,
#					"uid": 1000,
#					"user": "woodoo"
#			},
#			...
#			{
#					"args": "/usr/share/code/resources/app/extensions/json-language-features/server/dist/jsonServerMain --node-ipc --clientProcessId=15491",
#					"cmd": "/usr/share/code/code",
#					"pid": 29554,
#					"ppid": 15491,
#					"stat": "Sl",
#					"time": "0:05",
#					"tty": null,
#					"uid": 1000,
#					"user": "woodoo"
#			},
#			{
#					"args": "--spawner :1.9 /org/gtk/gvfs/exec_spaw/6",
#					"cmd": "/usr/lib/gvfs/gvfsd-mtp",
#					"pid": 31616,
#					"ppid": 1,
#					"stat": "Sl",
#					"time": "0:25",
#					"tty": null,
#					"uid": 1000,
#					"user": "woodoo"
#			}
#	]
#
def get_ps(c = None) -> dict:
	stdout, stderr, exitcode = run(c, "ps axj")
	return parse_ps(stdout, stderr, exitcode)
#










