

import re

from .parsing_utils import *
from .invoke_utils import run



#
# Returns:
#
#	{
#		"install": [
#			"containerd",
#			"linux-headers-4.4.0-159",
#			"linux-headers-4.4.0-159-generic",
#			"linux-image-4.4.0-159-generic",
#			"linux-modules-4.4.0-159-generic",
#			"linux-modules-extra-4.4.0-159-generic",
#			"runc"
#		],
#		"remove": [],
#		"unnecessary": [],
#		"upgrade": [
#			"apparmor",
#			"apport",
#			"apport-gtk",
#			"apt",
#			...
#		]
#	}
#
def parse_apt_list(stdout:str, stderr:str, exitcode:int) -> dict:

	"""
	NOTE: This is only a simulation!
	      apt-get needs root privileges for real execution.
	      Keep also in mind that locking is deactivated,
	      so don't depend on the relevance to the real current situation!
	Reading package lists...
	Building dependency tree...
	Reading state information...
	Calculating upgrade...
	The following NEW packages will be installed:
	  containerd linux-headers-4.4.0-159 linux-headers-4.4.0-159-generic
	  linux-image-4.4.0-159-generic linux-modules-4.4.0-159-generic
	  linux-modules-extra-4.4.0-159-generic runc
	The following packages will be upgraded:
	  apparmor apport apport-gtk apt apt-transport-https apt-utils aptdaemon
	  aptdaemon-data bash btrfs-tools bzip2 chromium-codecs-ffmpeg-extra cups
	  cups-bsd cups-client cups-common cups-core-drivers cups-daemon cups-ppdc
	  cups-server-common dbus dbus-x11 dh-python docker.io dpkg dpkg-dev firefox
	  firefox-locale-en flashplugin-installer fonts-opensymbol friendly-recovery
	  fwupd ghostscript ghostscript-x gvfs gvfs-backends gvfs-bin gvfs-common
	  gvfs-daemons gvfs-fuse gvfs-libs imagemagick imagemagick-6.q16
	  imagemagick-common intel-microcode libapparmor-perl libapparmor1
	  libapt-inst2.0 libapt-pkg5.0 libbz2-1.0 libcups2 libcups2:i386 libcupscgi1
	  libcupsimage2 libcupsmime1 libcupsppdc1 libdb5.3 libdb5.3:i386 libdbus-1-3
	  libdbus-1-3:i386 libdbus-1-dev libdfu1 libdpkg-perl libebml4v5 libelf1
	  libelf1:i386 libexiv2-14 libexpat1 libexpat1:i386 libexpat1-dev libfwupd1
	  libgif7 libgif7:i386 libglib2.0-0 libglib2.0-bin libglib2.0-data
	  libglib2.0-dev libgs9 libgs9-common libimage-magick-perl
	  libimage-magick-q16-perl libldap-2.4-2 libldap-2.4-2:i386
	  libmagick++-6.q16-5v5 libmagickcore-6.q16-2 libmagickcore-6.q16-2-extra
	  libmagickwand-6.q16-2 libmosquitto1 libmspack0 libmysqlclient20 libnss3
	  libnss3-nssdb libopenjp2-7 libpam-systemd libpoppler-glib8 libpoppler58
	  libpq5 libqt5core5a libqt5dbus5 libqt5gui5 libqt5libqgtk2 libqt5network5
	  libqt5opengl5 libqt5printsupport5 libqt5sql5 libqt5sql5-sqlite
	  libqt5widgets5 libqt5xml5 librados2 librbd1
	  libreoffice-avmedia-backend-gstreamer libreoffice-base-core libreoffice-calc
	  libreoffice-common libreoffice-core libreoffice-draw libreoffice-gnome
	  libreoffice-gtk libreoffice-impress libreoffice-math libreoffice-ogltrans
	  libreoffice-pdfimport libreoffice-style-breeze libreoffice-style-galaxy
	  libreoffice-style-human libreoffice-writer libsndfile1 libsndfile1:i386
	  libsox-fmt-alsa libsox-fmt-base libsox2 libsqlite3-0 libsqlite3-0:i386
	  libsvn1 libsystemd0 libsystemd0:i386 libudev-dev libudev1 libudev1:i386
	  libvirt-bin libvirt0 libwhoopsie0 libzmq5 linux-firmware linux-generic
	  linux-headers-generic linux-image-generic linux-libc-dev makemkv-bin
	  makemkv-oss mosquitto mosquitto-clients mysql-client-5.7
	  mysql-client-core-5.7 mysql-common mysql-server mysql-server-5.7
	  mysql-server-core-5.7 nginx nginx-common nginx-core openjdk-8-jre
	  openjdk-8-jre-headless patch php7.0 php7.0-cli php7.0-common php7.0-dev
	  php7.0-fpm php7.0-gd php7.0-intl php7.0-json php7.0-mbstring php7.0-mysql
	  php7.0-opcache php7.0-readline php7.0-sqlite3 php7.0-xml
	  policykit-desktop-privileges poppler-utils python-apt-common python3-apport
	  python3-apt python3-aptdaemon python3-aptdaemon.gtk3widgets
	  python3-aptdaemon.pkcompat python3-problem-report
	  python3-software-properties qemu qemu-block-extra qemu-kvm qemu-system
	  qemu-system-arm qemu-system-common qemu-system-mips qemu-system-misc
	  qemu-system-ppc qemu-system-sparc qemu-system-x86 qemu-user qemu-user-binfmt
	  qemu-utils redis-server redis-tools snapd software-properties-common
	  software-properties-gtk sox sqlite3 subversion sudo systemd systemd-sysv
	  thunderbird thunderbird-locale-en thunderbird-locale-en-us tzdata
	  ubuntu-core-launcher ubuntu-minimal ubuntu-standard udev uno-libs3 ure
	  usb-creator-common usb-creator-gtk vim vim-common vim-runtime vim-tiny
	  whoopsie xul-ext-calendar-timezones xul-ext-gdata-provider xul-ext-lightning
	233 upgraded, 7 newly installed, 0 to remove and 0 not upgraded.
	Inst bash [4.3-14ubuntu1.3] (4.3-14ubuntu1.4 Ubuntu:16.04/xenial-updates, Ubuntu:16.04/xenial-security [amd64])
	Conf bash (4.3-14ubuntu1.4 Ubuntu:16.04/xenial-updates, Ubuntu:16.04/xenial-security [amd64])
	Inst dpkg [1.18.4ubuntu1.5] (1.18.4ubuntu1.6 Ubuntu:16.04/xenial-updates [amd64])
	Conf dpkg (1.18.4ubuntu1.6 Ubuntu:16.04/xenial-updates [amd64])
	Inst bzip2 [1.0.6-8] (1.0.6-8ubuntu0.2 Ubuntu:16.04/xenial-updates, Ubuntu:16.04/xenial-security [amd64]) []
	....
	Conf xul-ext-gdata-provider (1:60.8.0+build1-0ubuntu0.16.04.2 Ubuntu:16.04/xenial-updates, Ubuntu:16.04/xenial-security [amd64])
	Conf libopenjp2-7 (2.1.2-1.1+deb9u3build0.16.04.1 Ubuntu:16.04/xenial-updates, Ubuntu:16.04/xenial-security [amd64])
	"""
	
	if exitcode != 0:
		raise Exception()

	lines = stdout.strip().split("\n")

	startPos = -1
	for startPos, line in enumerate(lines):
		if line == "Reading package lists...":
			break
	if startPos < 0:
		raise Exception()

	lines = lines[startPos:]

	endPos = -1
	for endPos, line in enumerate(lines):
		if line.endswith(" not upgraded."):
			break
	if endPos < 0:
		raise Exception()

	lines = lines[:endPos+1]

	ret = groupLinesByLeadingSpace(lines)
	for k, v in ret.items():
		ret2 = []
		for line in v:
			for s in line.split(" "):
				if s:
					ret2.append(s)
		ret[k] = ret2

	ret3 = {
		"install": [],
		"remove": [],
		"upgrade": [],
		"unnecessary": [],
	}
	for linePatternType, linePattern, key in (
			(1, "The following NEW packages will be installed:", "install"),
			(1, "The following additional packages will be installed:", "install"),
			(1, "The following packages will be REMOVED:", "remove"),
			(1, "The following packages will be upgraded:", "upgrade"),
			(1, "The following packages were automatically installed and are no longer required:", "unnecessary"),
		):

		if linePatternType == 1:
			# exact
			v = ret.get(linePattern)
			if v is not None:
				ret3[key] = ret3[key] + v
				del ret[linePattern]
		else:
			raise Exception()

	for key in list(ret.keys()):
		if key.endswith(" not upgraded."):
			del ret[key]
			continue
		if key.endswith("..."):
			del ret[key]
			continue

	if ret:
		raise Exception("Unknown keys: " + ", ".join(ret.keys()))

	ret4 = {}
	for k, v in ret3.items():
		ret4[k] = sorted(set(v))

	return ret4
#



#
# Returns:
#
#	{
#		"install": [
#			"containerd",
#			"linux-headers-4.4.0-159",
#			"linux-headers-4.4.0-159-generic",
#			"linux-image-4.4.0-159-generic",
#			"linux-modules-4.4.0-159-generic",
#			"linux-modules-extra-4.4.0-159-generic",
#			"runc"
#		],
#		"remove": [],
#		"unnecessary": [],
#		"upgrade": [
#			"apparmor",
#			"apport",
#			"apport-gtk",
#			"apt",
#			...
#		]
#	}
#
def get_apt_list(c = None) -> dict:
	stdout, stderr, exitcode = run(c, "/usr/bin/apt-get -s dist-upgrade")
	return parse_apt_list(stdout, stderr, exitcode)
#


















