import matplotlib.pyplot as plt
from ErrorSegment import ErrorSegment
from Arff import Arff
import util
#TODO This is not a good name
class ErrorSegments():
   def __init__(self,error_segments):
      self.error_segments = error_segments
      self.arff = Arff()

   def most_different(self):
      new_error_segments = []
      index_error_segment = 0
      for error_segment in self.error_segments:
	 index_segments = 0
	 for segments in error_segment.segments:
	    if index_segments == error_segment.correct_index[index_segments]:
	       continue

	    index_segment = 0
	    #[:][margin][index]
	    margins = []
#	    print error_segment.file_name[index_segments]
#	    print len(segments)
	    for segment in segments[0]:
	       margin = (segment.score -
		     segments[error_segment.correct_index[index_segments]]
			   [index_segment].score)
	       margins.append([margin, index_segment])
#	       print str(margin) + ' ' + segment.state + ' ' +\
#		     segments[error_segment.correct_index[index_segments]]\
#			[index_segment].state
	       index_segment += 1

	    margins.sort(reverse=False)
	    for margin in margins:
	       if margin[0] > 0:
		  break
	       #if the states of the max margin is the same continue
	       if segments[error_segment.correct_index[index_segments]]\
		     [margin[1]].state == segments[0][margin[1]].state:
		  continue

	       samples = dict()
	       biggest = segments[0][margin[1]].score
	       new_segments = []
	       for segment in segments:
		  new_segments.append([segment[margin[1]]])
		  #the segment is not the first and not the recognized?
		  if segment != segments[0] and \
			segment != segments[error_segment.correct_index[index_segments]]:
		     #the phoneme was already analysed
		     if samples.has_key(segment[margin[1]].state):
			#if the stored score is biggest than the actual score throw away
			if samples[segment[margin[1]].state] > segment[margin[1]].score:
			   continue
		  samples[segment[margin[1]].state] = segment[margin[1]].score
		  if biggest < segment[margin[1]].score:
		     biggest = segment[margin[1]].score

	       for samples_key in samples:
		  samples[samples_key] = biggest / samples[samples_key]
	       samples['confusao'] = 'sim'

	       new_error_segment = ErrorSegment(new_segments,
			error_segment.correct_index[index_segments],
			error_segment.start_time[index_segments]+margin[1],
			error_segment.file_name[index_segments])

	       if (new_error_segment.correct_states == 'v[4]' and
		     new_error_segment.recognized_states == 'ow1[4]'):
		  self.arff.add(samples)

		  util.add_error_segment(new_error_segments,
			new_error_segment)
	       break
	    index_segments += 1
	 index_error_segment += 1

#      self.arff.write('out.arff')
#      print self.arff
      for error_segment in new_error_segments:
	 if len(error_segment.segments):# > 20:
	    print str(error_segment) + ' qtd ' + str(len(error_segment.segments))
	    for file_name in error_segment.file_name:
	       print file_name
      return new_error_segments, self.arff
