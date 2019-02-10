'''
Utility functions that print out information if specified in the settings file.
'''
def printIfNeeded(data, constants):
	if constants.getValue("printdata") and not constants.getValue("tuneHSV"):
		print(data)

def printIfNeededHSV(data, constants):
	if constants.getValue("tuneHSV"):
		print(data)
