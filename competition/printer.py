'''
A utility function that prints out information if specified in the settings file.
'''
def printIfNeeded(data, constants):
	if constants.getValue("printdata"):
		print(data)
