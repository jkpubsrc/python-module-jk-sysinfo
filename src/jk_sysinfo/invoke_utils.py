
import os
import subprocess
import typing

try:
	from fabric import Connection
except ImportError as ee:
	pass



_debuggingEnabled = False

def enableDebugging():
	global _debuggingEnabled

	_debuggingEnabled = True
#





#
# Run a command locally or remotely.
# If a "cat <file>" is to be invoked *and* this is to be invoked locally, this method will detect this. In that case instead of running "cat" it will fall back to a regular file read
# for efficiency. Therefore you can access data on local and remote systems in a uniform way without spending too much thoughts on efficiency.
#
# @param		fabric.Connection c				(optional) Provide a fabric connection here if you want to run a command remotely.
#												If you specify <c>None</c> here the command will be run locally.
# @param		str command						(required) The command to run. Please note that this command will be interpreted by a shell.
# @param		bool failOnNonZeroExitCode		(optional) Raises an exception if the last command executed returned with a non-zero exit code.
#
#
def run(c, command:str, failOnNonZeroExitCode:bool = True) -> typing.Union[str,str,int]:
	global _debuggingEnabled

	if c is None:
		if command.startswith("cat "):
			filePath = command[4:]
			if _debuggingEnabled:
				print("Using standard file reading for command: " + repr(command))
			if os.path.isfile(filePath):
				with open(filePath, "r", encoding="UTF-8", newline="\n") as f:
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












