#! /usr/bin/python

import argparse
import os

from Parser import Parser
from XmlHelper import XmlHelper
from Helpers import initGlobals, goToFailure, trace
from Flattener import Flattener


def assemble(filters):
	'''Convert a list of Filters to an XML document with each Filter as an entry.'''
	assert isinstance(filters, list)
	xml = XmlHelper()
	
	for filter in filters:
		entry = filter.assemble()
		if entry:
			xml.addEntry(entry)
	return str(xml)

	
def main(inFile, outFile, exitAfterParsing):
	contents = inFile.read()
	
	# Parse the input into something like an AST with abstractions
	# for Matchers and Actions in a tree structure.
	filters = Parser().parse(contents)

	if exitAfterParsing:
		return
	# Flatten out the tree such that there is a filter for every node in the tree.
	
	finalFilters = Flattener().flatten(filters)
	
	# convert the filters to XML
	xml = assemble(finalFilters) 

	trace("The generated xml output is as follows:\n%s" % xml)

	try:	
		outFile = open(outFile, 'w+')
	except:
		print("Cannot open the output file '{}'".format(args.output_file))
		exit(1)

	outFile.write(xml)
	outFile.close()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Generate XML for email filters.')
	parser.add_argument( 'input_file', help="The file containing the rules to generate filters.")
	parser.add_argument( 'output_file', help="The file to output the filter in XML")
	parser.add_argument('-t', '--trace', action='store_true', help='Add tracing')
	parser.add_argument('--pdb', action='store_true', help='Catch failures in pdb.')
	# Only to be used when testing catching syntax errors
	parser.add_argument('--ignoreParseErrors', action='store_true', 
											help=argparse.SUPPRESS)
											
	args = parser.parse_args()
	
	initGlobals(args.pdb, args.trace, args.ignoreParseErrors)
	
	# If the trace argument was provided then this will be printed
	trace("Tracing is turned on for this run.")
	
	try:
		inFile = open(args.input_file, "r")
	except:
		print("The input file '{}' does not exits.".format(args.input_file))
		exit(-1)
	
	try:
		main(inFile, args.output_file, args.ignoreParseErrors)
	except Exception as e:
		print(e)
		
	trace("Finished, closing files.")
	inFile.close()