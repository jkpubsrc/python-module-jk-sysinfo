
import os
import subprocess

try:
	from fabric import Connection
except ImportError as ee:
	pass



_debuggingEnabled = False

def enableDebugging():
	global _debuggingEnabled

	_debuggingEnabled = True
#





def run(c, command, failOnNonZeroExitCode:bool = True):
	global _debuggingEnabled

	if c is None:
		if command.startswith("cat "):
			filePath = command[4:]
			if _debuggingEnabled:
				print("Using standard file reading for command: " + repr(command))
			if os.path.isfile(filePath):
				with open(filePath, "r") as f:
					return f.read(), "", 0
			else:
				raise Exception("No such file: " + repr(filePath))
		if _debuggingEnabled:
			print("Invoking via subprocess: " + repr(command))
		p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		binStdOut, binStdErr = p.communicate()
		stdOut = binStdOut.decode("utf-8")
		stdErr = binStdErr.decode("utf-8")
		if _debuggingEnabled:
			print("exit status:", p.returncode)
			print("stdout:")
			for line in stdOut.split("\n"):
				print("\t" + repr(line))
			print("stderr:")
			for line in stdErr.split("\n"):
				print("\t" + repr(line))
		if failOnNonZeroExitCode and p.returncode > 0:
			raise Exception("Command failed with exit code " + str(p.returncode) + ": " + repr(command))
		return stdOut, stdErr, p.returncode

	if (c.__class__.__name__ == "Connection") and (c.__class__.__module__ in [ "fabric", "fabric.connection" ]):
		if _debuggingEnabled:
			print("Invoking via fabric: " + repr(command))
		r = c.run(command, hide=True)
		if _debuggingEnabled:
			print("exit status:", r.exited)
			print("stdout:")
			for line in r.stdout.split("\n"):
				print("\t" + repr(line))
			print("stderr:")
			for line in r.stderr.split("\n"):
				print("\t" + repr(line))
		if failOnNonZeroExitCode and r.exited > 0:
			raise Exception("Command failed with exit code " + str(r.exited) + ": " + repr(command))
		return r.stdout, r.stderr, r.exited

	raise Exception("Sorry, I don't know about " + repr(c.__class__) + " objects for parameter c.")
#












