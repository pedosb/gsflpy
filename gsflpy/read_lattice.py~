#! /usr/bin/env python
import sys

class ReadLattice():
    COMMENT_CHAR = '#'

    def error(self, comment):
	print comment
	exit(-1)

    def parse_node_and_link_number(self, line):
	line_splitted = line.split()

	words = line_splitted[0].split('=')
	if words[0] != 'N':
	    error('expected N, but was found "' +\
		    words[0] + '"')
	self.node_number = words[1]

        words = line_splitted[1].split('=')
	if words[0] != 'L':
	    error('expected L, but was found "' + \
		    words[0] + '"')
	self.link_number = words[1]

    def parse_line(self, line):
	arg_type = line.split()[0].split('=')[0]
	if arg_type == 'N':
	    self.parse_node_and_link_number(line)
	else:
	    error('not found argument "' + \
		    arg_type + '"')

    def parse(self, lat_file):
	for line in open(lat_file):
	    if line.startswith(self.COMMENT_CHAR):
		continue
	    if line.split()[0].split('=')[0] == 'N':
		self.parse_line(line)
	print self.node_number
	print self.link_number

if __name__ == "__main__":
    read = ReadLattice()
    read.parse(sys.argv[1])
