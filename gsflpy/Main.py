#! /usr/bin/env python
import sys
from ReadLattice import ReadLattice
from Sentence import Sentence
from ErrorSegment import ErrorSegment
from ErrorSegments import ErrorSegments

def usage():
   print 'Usage: ' + sys.argv[0] + ' ' +\
	 '(((-l <lattice_file> ' +\
	 '[-w <int_number>] ' +\
	 '[-c <string>] ' +\
	 '[-o <figure.png>]) | ' +\
	 '(-L <lattice_and_transcriptions_file_path> ' + \
	 '[-p <figure_sufix>])) | ' +\
	 '[-f <in_error_file>]) | ' +\
	 '[-F <out_error_file>] ' +\
	 '[-v]'
   print '  -l: File that contains the lattice.'
   print '  -L: File that contains the path for lattice file (whithout spaces)'
   print '      followed by the number of max words and then correct transcription (one per line).'
   print '  -w: Max number of nodes per sentence.'
   print '  -s: Max score diff (for prunning).'
   print '  -c: Correct sentence.'
   print '  -F: File to write the correct and the recognized sentences with they score.'
   print '  -f: File with the recognized sentences'
   print '  -o: Name of a file to store the figure (png).'
   print '  -p: sufix to be appended in the name of the latttice and write the' +\
        ' png file as output.'
   print '  -v: Show more status information.'
   exit(-1)

def find_correct(sentences, correct_sentence):
   count = 0
   for sentence in sentences:
      if str(sentence) == correct_sentence:
	 return sentence, count
      count += 1

   return None, None

def plot():
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
		     for i in range(int(segment.length*100)):
			if not last_state:
			   last_state = segment.state
			   count_state = 0
			   initial_point = len(sentence.score_points)
			   sentence.state_transition_points.append([initial_point, segment.score])
			elif last_state == segment.state:
			   count_state += 1
			else:
			   x_point = (count_state / 2) + initial_point
			   sentence.states_points.append([last_state, \
				 x_point, sentence.score_points[x_point]])
			   last_state = None
			sentence.score_points.append(segment.score)
	    plot_setting = ''
	    if sentence == correct_sentence:
	       color = 'c'
	       plot_setting += 'g'
	    else:
	       color = 'r'
	       plot_setting += 'b'

	    for points in sentence.state_transition_points:
	       plt.plot(points[0], points[1], 'o' + plot_setting, ms=8)
	    for points in sentence.states_points:
	       plt.text(points[1], \
		     points[2], \
		     str(points[0]), \
		     dict(color=color, \
		       size='12', \
		       weight='semibold'))
	    plt.plot(sentence.score_points, \
		  plot_setting, \
		  label=str(sentence), \
		  linewidth=1.5)

      plt.ylabel('score')
      plt.xlabel('time')
      plt.legend()
      if OUT_FIGURE:
	 plt.savefig(OUT_FIGURE, orientation='landscape', format='png', papertype='a0')
      else:
	 plt.show()

def plot_error_segment(error_segments):
   time_count = 0
   time_sum = 0
   for error_segment in error_segments:
      for correct_segment in error_segment.correct_segments:
#	 print error_segment.file_name
#	 print len(correct_segment)
	 time_sum += len(correct_segment)
	 time_count += 1
	 
   import math
   import numpy as np
   import matplotlib.pyplot as plt
   import matplotlib.mlab as mlab

   time_mean = time_sum / time_count
   time_var = 0
   for error_segment in error_segments:
      for correct_segment in error_segment.correct_segments:
	 time_var += math.pow(\
	       (len(correct_segment) - time_mean), 2)
   time_var = time_var / time_count

   print 'mean ' + str(time_mean)
   print 'var ' + str(time_var)
   print 'sum ' + str(time_sum)
   figure = plt.figure(figsize=(20,15), dpi=200)
   x = np.arange(-time_var*5, time_var*5, 0.1)
   y = mlab.normpdf(x, time_mean, time_var)
   plt.xlabel('time')
   plt.grid(True)
   plt.plot(x,y)
   plt.savefig('gauss')

   y = []
   figure = plt.figure(figsize=(60,35), dpi=700)
   plt.grid(True)
   for error_segment in error_segments:
      y.append(len(error_segment.correct_segments))
   plt.plot(y)
   plt.ylabel('times')
   plt.xlabel('id')
   plt.savefig('times')
#   plt.show()

def write_error_segmets(error_segments):
   file_out = open(ERROR_SEGMENTS_OUT_FILE, 'w')
   for error_segment in error_segments:
      i = 0
      for segments in error_segment.segments:
	 file_out.write(str(error_segment.file_name[i]))
	 file_out.write(';')
	 file_out.write(str(error_segment.start_time[i]))
	 file_out.write(';')
	 file_out.write(str(error_segment.correct_index[i]))
	 for segment in segments:
	    file_out.write(';:')
	    for segment_unit in segment:
	       file_out.write(str(segment_unit))
	 file_out.write(';\n')
	 i += 1
   file_out.flush()
   file_out.close()

if __name__ == "__main__":
   LAT_FILE = None
   MAX_NODE = None
   CORRECT_SENTENCE = None
   OUT_FIGURE = None
   VERBOSE = None
   MAX_SCORE_DIFF = None
   MAX_FRAME_DIFF = None
   ERROR_SEGMENTS_OUT_FILE = None
   ERROR_SEGMENTS_IN_FILE = None

   if len(sys.argv) == 1:
      usage()

   count = 1
   while count < len(sys.argv):
      if sys.argv[count][0] == '-':
	 if sys.argv[count][1] == 'l':
	    LAT_FILE = sys.argv[count+1]
	 elif sys.argv[count][1] == 'L':
	    LAT_FILE = []
	    MAX_NODE = []
	    CORRECT_SENTENCE = []
	    for line in open(sys.argv[count+1]):
	       words = line.split()
	       LAT_FILE.append(words[0])
	       MAX_NODE.append(words[1])
	       sentence = ""
	       for word in words[2:len(words)]:
		  sentence += word + ' '
	       CORRECT_SENTENCE.append(sentence.strip())
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
	 elif sys.argv[count][1] == 'F':
	    ERROR_SEGMENTS_OUT_FILE = str(sys.argv[count+1])
	 elif sys.argv[count][1] == 'f':
	    ERROR_SEGMENTS_IN_FILE = str(sys.argv[count+1])
	 else:
	    usage()
	 count += 2
      else:
	 usage()
   if ERROR_SEGMENTS_IN_FILE:
      read = ReadLattice(VERBOSE=VERBOSE)
      error_segments = read.parse_error_segment_file(ERROR_SEGMENTS_IN_FILE)
#      write_error_segmets(error_segments)
#      for error_segment in error_segments:
#	 print str(error_segment) + ' qtd ' + str(len(error_segment.correct_segments))
      err = ErrorSegments(error_segments)
      err.most_different()

   elif isinstance(LAT_FILE, list):
      index = 0
      error_segments = []
      for lat_file in LAT_FILE:
	 read = ReadLattice(VERBOSE=VERBOSE)
	 lattice = read.parse(lat_file)
	 sentences = lattice.search_sentences_c(MAX_NODE[index])
	 if len(sentences) < 1:
	    print 'WARNING: No sentences found'
	 else:
	    print 'Recognized:'
	    print str(sentences[0]) + ' ' + str(sentences[0]._score)
	    correct_sentence, number = find_correct(sentences, \
		  CORRECT_SENTENCE[index])
	    if not correct_sentence:
	       print 'WARNING: Correct sentence not found!!!'
	    else:
	       print 'Correct was the sentence number ' + str(number + 1) + ':'
	       print str(correct_sentence) + '  ' + \
		     str(correct_sentence._score)
#	       print lat_file
#	       plot()
	       error_segments = lattice.get_error_segments(number, error_segments) 
	       if VERBOSE:
		  for error_segment in error_segments:
		     print str(error_segment) + ' qtd ' + str(len(error_segment.correct_segments))
	       print index
	       del lattice, read, sentences
	 index += 1
      #plot_error_segment(error_segments)
      for error_segment in error_segments:
	 print str(error_segment) + ' qtd ' + str(len(error_segment.segments))
      write_error_segmets(error_segments)
   else:
      read = ReadLattice(VERBOSE=VERBOSE)
      lattice = read.parse(LAT_FILE)
      sentences = lattice.search_sentences_c(MAX_NODE)
      print 'Recognized:'
      print str(sentences[0]) + '  ' + str(sentences[0]._score)
      if CORRECT_SENTENCE:
	 correct_sentence, number = find_correct(sentences, CORRECT_SENTENCE)
	 if not correct_sentence:
	    print 'WARNING: Correct sentence not found!!!'
	 else:
	    print 'Correct was the sentence number ' + str(number + 1) + ':'
	    print str(correct_sentence) + '  ' + \
		  str(correct_sentence._score)
	    plot()

	 error_segments = lattice.get_error_segments(number)
	 for error_segment in error_segments:
	    print str(error_segment) + ' qtd ' + str(len(error_segment.correct_segments))
