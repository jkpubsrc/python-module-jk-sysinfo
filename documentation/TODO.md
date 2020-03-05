* TODO: `sysinfo.py` avoids calling `get_motherboard_info()` on Raspberry Pi devices thus working around getting the desired information this way.
	* Reason: Completely different approaches need to be taken in order to get motherboard information on Raspberry Pi.
	* We might want to find a unifying solution, abstracting away from specific file and tool details.
	* The question is: Are these get-functions lower level or higher level? If lower level: Directly wrap around system files and tools and don't abstract away from them. If higher level: We can abstract but than we might want to make clear it is an abstraction.
	* Possible solution: Split into two directories: lower level functions and higher level functions.




