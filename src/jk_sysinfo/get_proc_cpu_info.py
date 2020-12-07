
import typing

from jk_cachefunccalls import cacheCalls
from jk_cmdoutputparsinghelper import ValueParser_ByteWithUnit

from .parsing_utils import *
from .invoke_utils import run
#import jk_json



_parserColonKVP = ParseAtFirstDelimiter(delimiter=":", valueCanBeWrappedInDoubleQuotes=False, keysReplaceSpacesWithUnderscores=True)



#
# Returns:
#
#	[
#		{
#			"<key>": "<value>",
#			...
#		},
#		...
#	]
#
def parse_proc_cpu_info(stdout:str, stderr:str, exitcode:int) -> typing.Tuple[list,dict]:

	"""
	processor	: 0
	vendor_id	: GenuineIntel
	cpu family	: 6
	model		: 92
	model name	: Intel(R) Pentium(R) CPU J4205 @ 1.50GHz
	stepping	: 9
	microcode	: 0x38
	cpu MHz		: 1000.000
	cache size	: 1024 KB
	physical id	: 0
	siblings	: 4
	core id		: 0
	cpu cores	: 4
	apicid		: 0
	initial apicid	: 0
	fpu		: yes
	fpu_exception	: yes
	cpuid level	: 21
	wp		: yes
	flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg cx16 xtpr pdcm sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave rdrand lahf_lm 3dnowprefetch intel_pt ibrs ibpb stibp tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust smep erms mpx rdseed smap clflushopt sha_ni xsaveopt xsavec xgetbv1 dtherm ida arat pln pts md_clear arch_capabilities
	bugs		: monitor spectre_v1 spectre_v2
	bogomips	: 2995.20
	clflush size	: 64
	cache_alignment	: 64
	address sizes	: 39 bits physical, 48 bits virtual
	power management:

	processor	: 1
	vendor_id	: GenuineIntel
	cpu family	: 6
	model		: 92
	model name	: Intel(R) Pentium(R) CPU J4205 @ 1.50GHz
	stepping	: 9
	microcode	: 0x38
	cpu MHz		: 800.000
	cache size	: 1024 KB
	physical id	: 0
	siblings	: 4
	core id		: 1
	cpu cores	: 4
	apicid		: 2
	initial apicid	: 2
	fpu		: yes
	fpu_exception	: yes
	cpuid level	: 21
	wp		: yes
	flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg cx16 xtpr pdcm sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave rdrand lahf_lm 3dnowprefetch intel_pt ibrs ibpb stibp tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust smep erms mpx rdseed smap clflushopt sha_ni xsaveopt xsavec xgetbv1 dtherm ida arat pln pts md_clear arch_capabilities
	bugs		: monitor spectre_v1 spectre_v2
	bogomips	: 2995.20
	clflush size	: 64
	cache_alignment	: 64
	address sizes	: 39 bits physical, 48 bits virtual
	power management:

	processor	: 2
	vendor_id	: GenuineIntel
	cpu family	: 6
	model		: 92
	model name	: Intel(R) Pentium(R) CPU J4205 @ 1.50GHz
	stepping	: 9
	microcode	: 0x38
	cpu MHz		: 800.000
	cache size	: 1024 KB
	physical id	: 0
	siblings	: 4
	core id		: 2
	cpu cores	: 4
	apicid		: 4
	initial apicid	: 4
	fpu		: yes
	fpu_exception	: yes
	cpuid level	: 21
	wp		: yes
	flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg cx16 xtpr pdcm sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave rdrand lahf_lm 3dnowprefetch intel_pt ibrs ibpb stibp tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust smep erms mpx rdseed smap clflushopt sha_ni xsaveopt xsavec xgetbv1 dtherm ida arat pln pts md_clear arch_capabilities
	bugs		: monitor spectre_v1 spectre_v2
	bogomips	: 2995.20
	clflush size	: 64
	cache_alignment	: 64
	address sizes	: 39 bits physical, 48 bits virtual
	power management:

	processor	: 3
	vendor_id	: GenuineIntel
	cpu family	: 6
	model		: 92
	model name	: Intel(R) Pentium(R) CPU J4205 @ 1.50GHz
	stepping	: 9
	microcode	: 0x38
	cpu MHz		: 1100.000
	cache size	: 1024 KB
	physical id	: 0
	siblings	: 4
	core id		: 3
	cpu cores	: 4
	apicid		: 6
	initial apicid	: 6
	fpu		: yes
	fpu_exception	: yes
	cpuid level	: 21
	wp		: yes
	flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg cx16 xtpr pdcm sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave rdrand lahf_lm 3dnowprefetch intel_pt ibrs ibpb stibp tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust smep erms mpx rdseed smap clflushopt sha_ni xsaveopt xsavec xgetbv1 dtherm ida arat pln pts md_clear arch_capabilities
	bugs		: monitor spectre_v1 spectre_v2
	bogomips	: 2995.20
	clflush size	: 64
	cache_alignment	: 64
	address sizes	: 39 bits physical, 48 bits virtual
	power management:
	"""

	if exitcode != 0:
		raise Exception()

	cpuInfos = splitAtEmptyLines(stdout.split("\n"))
	retExtra = {}
	ret = []
	for group in cpuInfos:
		d = _parserColonKVP.parseLines(group)
		if "processor" not in d:
			for k, v in d.items():
				retExtra[k.lower()] = v
			continue

		if "cache_size" in d:
			d["cache_size_kb"] = ValueParser_ByteWithUnit.parse(d["cache_size"]) // 1024
			del d["cache_size"]

		if "bogomips" in d:
			d["bogomips"] = float(d["apicid"])
		elif "BogoMIPS" in d:
			d["bogomips"] = float(d["BogoMIPS"])
			del d["BogoMIPS"]

		if "bugs" in d:
			d["bugs"] = d["bugs"].split()

		if "flags" in d:
			d["flags"] = sorted(d["flags"].split())
		elif "Features" in d:
			d["flags"] = sorted(d["Features"].split())
			del d["Features"]

		# bool
		for key in [ "fpu", "fpu_exception", "wp" ]:
			if key in d:
				d[key.lower()] = d[key] == "yes"
				if key != key.lower():
					del d[key]

		# int
		for key in [ "CPU_architecture", "CPU_revision", "physical_id", "initial_apicid", "cpu_cores", "core_id", "clflush_size", "cache_alignment", "apicid" ]:
			if key in d:
				d[key.lower()] = int(d[key])
				if key != key.lower():
					del d[key]

		# float
		for key in [ "cpu_MHz" ]:
			if key in d:
				d[key.lower()] = float(d[key])
				if key != key.lower():
					del d[key]

		# str
		for key in [ "CPU_implementer", "CPU_part", "CPU_variant" ]:
			if key in d:
				d[key.lower()] = d[key]
				if key != key.lower():
					del d[key]

		d["processor"] = int(d["processor"])

		if "siblings" in d:
			d["siblings"] = int(d["siblings"])

		#jk_json.prettyPrint(d)
		ret.append(d)

	return ret, retExtra
#



#
# Returns:
#
#	[
#		{
#			"<key>": "<value>",
#			...
#		},
#		...
#	]
#
@cacheCalls(seconds=3, dependArgs=[0])
def get_proc_cpu_info(c = None) -> typing.Tuple[list,dict]:
	stdout, stderr, exitcode = run(c, "cat /proc/cpuinfo")
	return parse_proc_cpu_info(stdout, stderr, exitcode)
#







