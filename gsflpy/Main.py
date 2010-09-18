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

def find_correct(sentences):
   count = 0
   for sentence in sentences:
      if str(sentence) == CORRECT_SENTENCE:
	 return sentence, count
      count += 1

   return None, None

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
	    CORRECT_SENTENCE = sys.argv[count+1].strip()
	 else:
	    usage()
	 count += 2
      else:
	 usage()

   read = ReadLattice()
   lattice = read.parse(LAT_FILE)
   sentences = lattice.search_sentences(MAX_NODE)
   sentences.sort()
   print 'Recognized:'
   print str(sentences[0]) + '  ' + str(sentences[0]._score)
   if CORRECT_SENTENCE:
      correct_sentence, number = find_correct(sentences)
      if correct_sentence:
	 print 'Correct was the sentence number ' + str(number + 1)
	 print str(correct_sentence) + '  ' + \
	       str(correct_sentence._score)
      else:
	 print 'WARNING: Correct sentence not found!!!'

   if correct_sentence:
      for sentence in sentences:
	 if sentence == correct_sentence or sentence == sentences[0]:
	    sentence.plot = True
	 else:
	    sentence.plot = False

      import matplotlib.pyplot as plt
      for sentence in sentences:
	 if sentence.plot:
	    sentence.score_points = []
	    for link in sentence.links:
	       if link.d:
		  for segment in link.d:
		     for i in range(segment.length*100):
			sentence.score_points.append(segment.score)
	    plot_setting = ''
	    print sentence
	    if sentence == correct_sentence:
	       plot_setting += 'g'
	    plt.plot(sentence.score_points, plot_setting)
      plt.ylabel('score')
      plt.xlabel('time')
      plt.show()
