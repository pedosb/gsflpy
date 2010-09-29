#!/usr/bin/env python
import sys
if __name__=="__main__":
   f = open(sys.argv[2], 'w')
   for line in open(sys.argv[1]):
      words = line.split()
      f.write('/home/pedro/Downloads/digits16k/lat/' + words[0])
      f.write(' ' + str(len(words)+4))
      f.write(' !NULL SENT-START')
      for word in words[1:len(words)]:
	 f.write(' ' + word)
      f.write(' SENT-END !NULL\n')
   f.flush()
   f.close()
