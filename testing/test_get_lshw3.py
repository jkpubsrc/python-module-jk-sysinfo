#!/usr/bin/python3



import jk_sysinfo

import jk_json



#jk_sysinfo.enableDebugging()

result = jk_sysinfo.get_lshw()

def _process(data:dict):
	assert isinstance(data, dict)

	sClass = data["class"]
	del data["class"]
	identifier = data["id"]
	del data["id"]
	if "children" in data:
		children = data["children"]
		del data["children"]
	else:
		children = None

	x = {}
	x["_id"] = identifier
	_addAttributes(x, data)
	if children:
		#xC = {}
		#x["children"] = xC
		for child in children:
			k, v = _process(child)
			if k not in x:
				x[k] = []
			x[k].append(v)
	return sClass, x
#

def _addAttributes(x:dict, dictData:dict, bWithUnderScore:bool = True):
	assert isinstance(x, dict)
	assert isinstance(dictData, dict)

	for k, v in dictData.items():
		k2 = ("_" + k) if bWithUnderScore else k
		if k == "logicalname":
			xLN = []
			x[k2 + "s"] = xLN
			if isinstance(v, list):
				xLN.extend(v)
			else:
				xLN.append(v)
			continue
		if isinstance(v, list):
			raise Exception(k)
		if isinstance(v, dict):
			x2 = {}
			x[k2] = x2
			_addAttributes(x2, v, bWithUnderScore=(k not in [ "capabilities", "configuration" ]))
		else:
			x[k2] = v
#

kret, vret = _process(result)

jk_json.prettyPrint(vret)





