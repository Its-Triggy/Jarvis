import time

SPOOL_TIME = 5

import subprocess
import sys

toolDict = {"screwdriver":0, "hammer":1, "knife":2, "wrench":3, "pliers":4, "wire cutters":5}



def lower_tool(tool):
	
	print("\t\t\t\t\tstart lowering " + tool)
	time.sleep(5)
	print("\t\t\t\t\tstop lowering " + tool)

	
def raise_tool(tool):
	
	print("\t\t\t\t\tstart raising " + tool)
	time.sleep(5)
	print("\t\t\t\t\tstop raising " + tool)



for arg in sys.argv[1:]:
    if arg.lower().split(',')[0] == "lower":
    	lower_tool(arg.lower().split(',')[1])
    elif arg.lower().split(',')[0] == "raise":
    	raise_tool(arg.lower().split(',')[1])


