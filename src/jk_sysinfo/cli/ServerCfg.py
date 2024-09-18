

import typing

import jk_typing
import jk_json
import jk_prettyprintobj
import jk_pwdinput




class ServerCfg(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self,
			*args,
			host:str,
			port:int,
			user:str = None,
			pwd:str = None,
			keyFile:str = None,
			**kwargs,
		):
		
		assert not args
		assert not kwargs
		
		# ----
		
		self.host = host
		self.port = port
		self.user = user
		self.pwd = pwd
		self.keyFile = keyFile
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def hasPwd(self) -> bool:
		return bool(self.pwd)
	#

	@property
	def shouldConnectViaUserNamePwd(self) -> bool:
		return bool(self.user)
	#

	@property
	def shouldConnectViaKeyFile(self) -> bool:
		return bool(self.keyFile)
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"host",
			"port",
			"user",
			"pwd",
			"keyFile",
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def readPwdFromSTDINIfPwdMissing(self):
		if self.keyFile:
			return
		if not self.pwd:
			self.pwd = jk_pwdinput.readpwd("Password for " + self.user + "@" + self.host + ": ")
	#

	@staticmethod
	def fromJSON(jData:typing.Dict[str,typing.Any]):
		assert isinstance(jData, dict)
		for k in jData.keys():
			assert isinstance(k, str)
			assert k

		jData2 = dict(jData)
		# TODO

		return ServerCfg(**jData2)
	#

	@staticmethod
	def loadFromFile(filePath:str):
		with open(filePath, "r", encoding="UTF-8", newline="\n") as fin:
			return ServerCfg.fromJSON(jk_json.loadFromFile(filePath))
	#

#


