"""
	scan every file that is listed to be synced, calc hash and launch shell command if tracked file changes
	implements multi-threading
	TODO:
	somehow read the contents of `.gdrive` and know which directories are to be synced
	FUTURE:
	use hooks on file-system table to detect changes i.e. something like Voidtool's everything.exe using analyseMFT
"""

import os
import json
import hashlib
from concurrent.futures import ProcessPoolExecutor

BLOCK_SIZE = 16 * 1024

def calcHash(filePath):
	hashVal = hashlib.md5()
	try:
		fp = open(filePath, mode='rb')
	except:
		logging.log("filePath read denied")
	with fp:
		while True:
			x = fp.read(BLOCK_SIZE)
			if len(x) == 0:	break
			hashVal.update(x)
	return hashVal.hexdigest()

def _makeDict(filePath):
	md5 = calcHash(filePath)
	records[md5] = filePath
	return

def worker(targetDir):
	targetDir = os.path.abspath(targetDir)
	records = dict()
	for root, dirs, files in os.walk(targetDir, topdown=True,\
	onerror=False):
		files = [os.path.join(root, _) for _ in files]
		with ProcessPoolExecutor(max_workers=4) as many:
			many.map(_makeDict, files)
	return records

def compare():
