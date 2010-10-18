#! /usr/bin/env python
import sys
from ReadLattice import ReadLattice
from Sentence import Sentence, find_correct, get_sentences
from ErrorSegment import ErrorSegment
from ErrorSegments import ErrorSegments
from ConsoleOptions import ConsoleOptions

def usage():
   print (sys.argv[0]+' (-L <file> | (-l <file> -w <int> -c <sentence>))'+
	 ' [-F <file>]'+
	 ' [-isl]')
   print
#   print ('Usage: ' + sys.argv[0] + ' ' +
#	 '(((-l <lattice_file> ' +
#	 '[-w <int_number>] ' +
#	 '[-c <string>] ' +
#	 '[-o <figure.png>]) | ' 
#	 '(-L <lattice_and_transcriptions_file_path> ' + 
#	 '[-p <figure_sufix>])) | ' +
#	 '[-f <in_error_file>] ' +
#	 '[-A <arff_file>]) | ' +
#	 '[-F <out_error_file>] ' +
#	 '[-v]')
#   print '  -l: File that contains the lattice.'
#   print '  -L: File that contains the path for lattice file (whithout spaces)'
#   print '      followed by the number of max words and then correct transcription (one per line).'
#   print '  -A: Write output in an ARFF file.'
#   print '  -w: Max number of nodes per sentence.'
#   print '  -s: Max score diff (for prunning).'
#   print '  -c: Correct sentence.'
#   print '  -F: File to write the correct and the recognized sentences with they score.'
#   print '  -f: File with the recognized sentences'
#   print '  -o: Name of a file to store the figure (png).'
#   print '  -p: sufix to be appended in the name of the latttice and write the' +\
#        ' png file as output.'
#   print '  -t: Only create an arff of all frames of the input lattice'
#   print '  -v: Show more status information.'
#   exit(-1)
   pass

def plot():
      for sentence in sentences:
	 if sentence == correct_sentence or sentence == sentences[0]:
	    sentence.plot = True
	 else:
	    sentence.plot = False

      #TODO make the code below really plot with different colors
      #all sentences marked with 'plot' 'True'
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
   if not ERROR_SEGMENTS_OUT_FILE:
      return
   file_out = open(ERROR_SEGMENTS_OUT_FILE, 'a')
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

def remove_error_segments_out_file():
   if ERROR_SEGMENTS_OUT_FILE:
      try:
	 import os
	 os.remove(ERROR_SEGMENTS_OUT_FILE)
      except OSError:
	 pass

def handle_lat_file(lattice_ops,
      error_segments = None):
   sentences, correct_sentence_index, lattice = get_sentences(lattice_ops)
   if not sentences:
      return error_segments
   if error_segments == None:
      error_segments = []

   if correct_sentence_index == None:
      print 'ERROR: Can not do anything (correct sentence not found).' 
      STATS['correct_not_found'] += 1
      return error_segments

   if correct_sentence_index == 0:
      if IS_CORRECT_LATTICE:
	 for i in range(1,len(sentences)):
	    error_segments = lattice.get_error_segments(i, error_segments)
      else:
	 print ("WARNING: Correct regonized file but 'IS_CORRECT_LATTICE'" +
	       " is set to 'False'.")
      STATS['acc_files'] += 1
      pass
   else:
      if not IS_CORRECT_LATTICE:
	 error_segments = lattice.get_error_segments(correct_sentence_index, error_segments)
   return error_segments

def clean_and_write_error_segments(error_segments):
   for error_segment in error_segments:
      error_segment.clean()
      print str(error_segment) + ' qtd ' + str(len(error_segment.segments))
   write_error_segmets(error_segments)

def handle_lattice():
   if not LAT_FILE:
      return
   if not isinstance(LAT_FILE, list):
      return

   STATS['acc_files'] = 0
   STATS['correct_not_found'] = 0
   STATS['files_count'] = 0

   remove_error_segments_out_file()
   index = 0
   error_segments = []
   for lat_file in LAT_FILE:
      error_segments = handle_lat_file((lat_file, MAX_NODE[index], CORRECT_SENTENCE[index]),
	 error_segments)

      print index
      if index % 25 == 0:
	 clean_and_write_error_segments(error_segments)
	 del error_segments
	 error_segments = []
      index += 1
   STATS['files_count'] = index
   #plot_error_segment(error_segments)
   clean_and_write_error_segments(error_segments)

def handle_error_segments():
   read = ReadLattice(VERBOSE=VERBOSE)
   error_segments = read.parse_error_segment_file(ERROR_SEGMENTS_IN_FILE)
#      write_error_segmets(error_segments)
#      for error_segment in error_segments:
#	 print str(error_segment) + ' qtd ' + str(len(error_segment.correct_segments))
   err = ErrorSegments(error_segments, STATES_CONFUSION, IS_CORRECT_LATTICE,
	 CONFUSION)
   new_error_segments, arff = err.most_different()
   if ARFF_OUT_FILE:
      arff.write(ARFF_OUT_FILE)


if __name__ == "__main__":
   STATS=dict()
   LAT_FILE = None
   MAX_NODE = None
   CORRECT_SENTENCE = None
   OUT_FIGURE = None
   VERBOSE = None
   MAX_SCORE_DIFF = None
   MAX_FRAME_DIFF = None
   ARFF_OUT_FILE = None
   ERROR_SEGMENTS_OUT_FILE = None
   ERROR_SEGMENTS_IN_FILE = None
   CREATE_ARFF_FROM_ALL = None
   IS_CORRECT_LATTICE = False
   STATES_CONFUSION = None
   CONFUSION = False

   option = ConsoleOptions(sys.argv, usage=usage)

   OUT_FIGURE = option.get_option('o')
   IS_CORRECT_LATTICE = option.get_option('iscorrectlattice')
   STATES_CONFUSION = option.get_option('p')
   CONFUSION = option.get_option('C')

   ERROR_SEGMENTS_OUT_FILE = option.get_option('F')
   ERROR_SEGMENTS_IN_FILE = option.get_option('f')
   ARFF_OUT_FILE = option.get_option('A')

   LAT_FILE, MAX_NODE, CORRECT_SENTENCE = option.get_option('L')
   if LAT_FILE == None:
      LAT_FILE = option.get_option('l')
      if LAT_FILE != None:
	 MAX_NODE = option.get_option('w')
	 if MAX_NODE == None:
	    self.usage(error_options='w')
	 CORRECT_SENTENCE = option.get_option('c')
	 if CORRECT_SENTENCE == None or CORRECT_SENTENCE == '':
	    self.usage(error_options='c')
	 LAT_FILE = [LAT_FILE]
	 MAX_NODE = [MAX_NODE]
	 CORRECT_SENTENCE = [CORRECT_SENTENCE]

   option.check_all_read()

   if LAT_FILE:
      if ERROR_SEGMENTS_IN_FILE:
	 option.usage('ERROR: -f Cannot be used with -L')
      if STATES_CONFUSION:
	 option.usage('ERROR: -p Cannot be used with -L')
      if ARFF_OUT_FILE:
	 option.usage('ERROR: -A Cannot be used with -L')
      handle_lattice()

   elif ERROR_SEGMENTS_IN_FILE:
      if not STATES_CONFUSION:
	 option.usage('ERROR: Now we want specific models to work see -p')
      handle_error_segments()


   print '################################'
   print '# STATS'
   for (key, value) in STATS.items():
      print '#',key,'=',value
   print '################################'
