#! /usr/bin/env python
import sys
from ReadLattice import ReadLattice

def usage():
   print 'Usage: ' + sys.argv[0] + ' ' +\
	 '-l <lattice_file> ' +\
	 '[-w <int_number>] ' +\
	 '[-c <string>]'
   print '  -l: File that contains the lattice.'
   print '  -w: Max number of nodes per sentence.'
   print '  -c: Correct sentence.'
   exit(-1)

if __name__ == "__main__":
   LAT_FILE = None
   MAX_NODE = None
   CORRECT_SENTENCE = None

   if len(sys.argv) == 1:
      usage()

   count = 1
   while count < len(sys.argv):
      if sys.argv[count][0] == '-':
	 if sys.argv[count][1] == 'l':
	    LAT_FILE = sys.argv[count+1]
	 elif sys.argv[count][1] == 'w':
	    MAX_NODE = int(sys.argv[count+1])
	 elif sys.argv[count][1] == 'c':
	    CORRECT_SENTENCE = sys.argv[count+1]
	 else:
	    usage()
	 count += 2
      else:
	 usage()

   read = ReadLattice()
   lattice = read.parse(LAT_FILE)
   sentences = lattice.search_sentences(MAX_NODE)
   sentences.sort()
   print sentences[0]
   print sentences[1]
   print sentences[2]
   print sentences[3]
