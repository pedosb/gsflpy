#! /usr/bin/env python
import sys
from ReadLattice import ReadLattice
from Sentence import Sentence

def usage():
   print 'Usage: ' + sys.argv[0] + ' ' +\
	 '-l <lattice_file> ' +\
	 '[-w <int_number>] ' +\
	 '[-c <string>] ' +\
	 '[-o <figure.png>] ' +\
	 '[-v]'
   print '  -l: File that contains the lattice.'
   print '  -w: Max number of nodes per sentence.'
   print '  -s: Max score diff (for prunning).'
   print '  -c: Correct sentence.'
   print '  -o: Name of a file to store the figure (png).'
   print '  -v: Show more status information.'
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
   OUT_FIGURE = None
   VERBOSE = None
   MAX_SCORE_DIFF = None
   MAX_FRAME_DIFF = None

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
	 elif sys.argv[count][1] == 'o':
	    OUT_FIGURE = sys.argv[count+1].strip()
	 elif sys.argv[count][1] == 'v':
	    VERBOSE = True
	    count -= 1
	 elif sys.argv[count][1] == 's':
	    MAX_FRAME_DIFF = float(sys.argv[count+2])
	    MAX_SCORE_DIFF = float(sys.argv[count+1])
	    count += 1
	 else:
	    usage()
	 count += 2
      else:
	 usage()

   read = ReadLattice(VERBOSE=VERBOSE)
   lattice = read.parse(LAT_FILE)
   sentences = lattice.search_sentences_c(MAX_NODE)
#   sentences = lattice.search_sentences(max_words = MAX_NODE, \
#	 max_score_diff = MAX_SCORE_DIFF, \
#	 max_frame_diff = MAX_FRAME_DIFF)
   sentences.sort(Sentence.cmp_score, reverse=True)
#   for sentence in sentences:
#      print str(sentence)
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
	 if OUT_FIGURE:
	    figure = plt.figure(figsize=(20,15), dpi=200)
	 else:
	    figure = plt.figure()
	 for sentence in sentences:
	    if sentence.plot:
	       sentence.score_points = []
	       sentence.states_points = []
	       sentence.state_transition_points = []
	       last_state = None
	       for link in sentence.links:
		  if link.d:
		     for segment in link.d:
			for i in range(segment.length*100):
			   if not last_state:
			      last_state = segment.state
			      count_state = 0
			      initial_point = len(sentence.score_points)
			      sentence.state_transition_points.append([initial_point, segment.score])
			   elif last_state == segment.state:
			      count_state += 1
			   else:
			      x_point = (count_state / 2) + initial_point
			      sentence.states_points.append([last_state, x_point, sentence.score_points[x_point]])
			      last_state = None
			   sentence.score_points.append(segment.score)
	       plot_setting = ''
	       print sentence
	       if sentence == correct_sentence:
		  color = 'c'
		  plot_setting += 'g'
	       else:
		  color = 'r'
		  plot_setting += 'b'

	       for points in sentence.state_transition_points:
		  plt.plot(points[0], points[1], 'o' + plot_setting, ms=8)
	       for points in sentence.states_points:
		  plt.text(points[1], points[2], str(points[0]), dict(color=color, size='12', weight='semibold'))

	       plt.plot(sentence.score_points, plot_setting, label=str(sentence), linewidth=1.5)

	       print len(sentence.state_transition_points)
	       print len(sentence.states_points)
	 plt.ylabel('score')
	 plt.xlabel('time')
	 plt.legend()
	 if OUT_FIGURE:
	    plt.savefig(OUT_FIGURE, orientation='landscape', format='png', papertype='a0')
	 else:
	    plt.show()
