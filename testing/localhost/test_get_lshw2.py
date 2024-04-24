#!/usr/bin/python3



import jk_sysinfo

import jk_json
from jk_simplexml import *



#jk_sysinfo.enableDebugging()

result = jk_sysinfo.get_lshw()

def _process(data):
	sClass = data["class"]
	del data["class"]
	identifier = data["id"]
	del data["id"]
	if "children" in data:
		children = data["children"]
		del data["children"]
	else:
		children = None

	x = HElement(sClass)
	x.setAttributeValue("identifier", identifier)
	_addAttributesToXML(x, data)
	if children:
		#xC = x.createChildElement("children")
		#for child in children:
		#	xC.add(_process(child))
		for child in children:
			x.add(_process(child))
	return x
#

def _addAttributesToXML(x:HElement, dictData:dict):
	for k, v in dictData.items():
		if k == "logicalname":
			xLN = x.createChildElement("logicalnames")
			if isinstance(v, list):
				for logicalName in v:
					xLN.createChildElement("logicalname").setChildText(logicalName)
			else:
				xLN.createChildElement("logicalname").setChildText(v)
			continue
		if isinstance(v, list):
			raise Exception(k)
		if isinstance(v, dict):
			x2 = x.createChildElement(k)
			_addAttributesToXML(x2, v)
		else:
			x.setAttributeValue(k, str(v))
#

xRoot = _process(result)

xmlWriteSettings = XMLWriteSettings()
xmlWriteSettings.writeXmlHeader = True
with open("test_get_lshw2.xml", "w") as f:
	f.write(HSerializer.toXMLStr(xRoot, xmlWriteSettings))






