#!/usr/bin/python3

import datetime as dt

from botinterface import *
from coreinterface import *

import storage
from notice import Notice





# functions
def print_notices():
	for notice in storage.iter():
		print(notice, end='\n\n')
	return





# main
com = None
while True:
	com = get_command()
	if com is None:
		break
	execute(com)

exit(0)





# END
