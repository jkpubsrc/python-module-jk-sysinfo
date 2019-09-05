

from .parsing_utils import *
from .invoke_utils import run



_parserColonKVP = ParseAtFirstDelimiter(delimiter=":", valueCanBeWrappedInDoubleQuotes=False, keysReplacesSpacesWithUnderscores=True)



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
def parse_proc_cpu_info(stdout:str, stderr:str, exitcode:int) -> dict:

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
	ret = []
	for group in cpuInfos:
		d = _parserColonKVP.parseLines(group)

		d["cache_size_kb"] = parseKByteWithUnit(d["cache_size"])
		del d["cache_size"]

		d["wp"] = d["wp"] == "yes"

		d["apicid"] = int(d["apicid"])

		d["bogomips"] = float(d["apicid"])

		d["bugs"] = d["bugs"].split()

		d["cache_alignment"] = int(d["cache_alignment"])

		d["clflush_size"] = int(d["clflush_size"])

		d["core_id"] = int(d["core_id"])

		d["cpu_MHz"] = float(d["cpu_MHz"])

		d["cpu_cores"] = int(d["cpu_cores"])

		d["flags"] = sorted(d["flags"].split())

		d["fpu"] = d["fpu"] == "yes"

		d["fpu_exception"] = d["fpu_exception"] == "yes"

		d["initial_apicid"] = int(d["initial_apicid"])

		d["physical_id"] = int(d["physical_id"])

		d["processor"] = int(d["processor"])

		d["siblings"] = int(d["siblings"])

		ret.append(d)
	return ret
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
def get_proc_cpu_info(c = None) -> dict:
	stdout, stderr, exitcode = run(c, "cat /proc/cpuinfo")
	return parse_proc_cpu_info(stdout, stderr, exitcode)
#







