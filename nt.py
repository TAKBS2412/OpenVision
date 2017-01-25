import main

# Called when data changes in NetworkTables
def valueChanged(table, key, value, isNew):
  # If the roboRIO has sent a command to tell the raspberry pi to start vision processing
  if isNew and key == "picmd" and value == "startvision":
	  # Start vision processing
    main.main()

# Called by main when vision processing has returned data.
# Sends data back to the roboRIO as a string
def sendData(data):
  table.putString(str(data))
