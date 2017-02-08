"""
 A simple python script that contains all the helper/util functions. This functions can be used by other scripts.
"""
import json
import os
import csv
from operator import itemgetter
from datetime import datetime

TAG = 'Code/Python/Util :'

def getAbsFileName(fname):
	"""
		Returns the absolute file path of a file
	"""
	fileAbsPath=os.path.abspath(fname)
	return fileAbsPath