#!/usr/bin/env python

import sys

if __name__=='__main__':
   if len(sys.argv) != 4:
      print sys.argv[0],'mlf_file use_file out_file'
      sys.exit(-1)

   fout = open(sys.argv[3],'w')
   for file in open(sys.argv[2]):
      file = file.replace('\n','')
      read = False
      sentence = ''
      for line in open(sys.argv[1]):
	 line = line.replace('\n','')
	 if read:
	    if line != '.':
	       sentence += ' '+line
	    else:
	       break
	 if line == '.':
	    continue
	 if line.replace('"','').replace('*','').replace('.lab','').replace('/','') == file.replace('.lat','').replace('.txt',''):
	    read = True
      if read:
	 fout.write('/home/02007004071/lvcsr/digits16k/lat/'+file.replace('.txt','.lat'))
	 fout.write(' '+str(len(sentence.split())+5))
	 fout.write(' !NULL SENT-START ')
	 fout.write(sentence.strip())
	 fout.write(' SENT-END !NULL\n')
      else:
	 print 'WARNING file not found on MLF'
