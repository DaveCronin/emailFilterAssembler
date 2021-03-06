#! /usr/bin/python

import pdb

'''
This file contains general use helper functions that can are used throughout the project.
'''

def initGlobals(_setPDB, _setTrace, _ignoreParseErrors):
	'''Initialises global variables.'''
	global setPDB
	setPDB = _setPDB
	global setTrace
	setTrace = _setTrace
	global labelWarningOccured
	labelWarningOccured = False
	global ignoreParseErrors
	ignoreParseErrors = _ignoreParseErrors
	

def goToFailure(error=None):
	'''Wrapper for exit which prints an error and can trip pdb if set.'''
	if setPDB:
		pdb.set_trace()
	raise Exception(error)
	
def trace(str):
	'''Wrapper for tracing if set to trace '''
	if setTrace:
		print(str)
		
def handleParseError(lineNumber, line, error):
	'''Handles a parse error by formating line information and the error before exiting.'''
	if ignoreParseErrors:
		print("Line {0}: {1} => {2}".format(lineNumber, line, error))
	else:
		goToFailure(error="Line {0}: {1} => {2}".format(lineNumber, line, error))
	
def labelWarning(label):
	'''Handler for warning of nested labels, providing verbose output only the first time.'''
	global labelWarningOccured
	if labelWarningOccured:
		print("Warning, another potentially nested label '{}'\n".format(label))
	else:
		print("Warning, the label '{}' contains a '/' which you might be using to indicate"
					" nested/sub labels or folders. When uploading filters to gmail the importer"
					" treats the / as part of the label name, and creates the label as such.\n"
					"It does not create a nested label with this information. However if a nested"
					" label aleardy exists, it will use it. So please create any nested labels first"
					" manually in gmail. Regular labels will be created automatically on import.\n"
					"Sorry for the inconvenience this causes.\n".format(label))
		labelWarningOccured = True
		
def detailAssert(a, op, b):
	if not op(a, b):
		print("failed {} {} {}".format(a, op, b))
		exit(1)