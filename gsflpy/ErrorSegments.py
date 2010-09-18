import matplotlib.pyplot as plt
from ErrorSegment import ErrorSegment
import util
#TODO This is not a good name
class ErrorSegments():
   def __init__(self,error_segments):
      self.error_segments = error_segments

   def most_different(self):
      index_error_segment = 0
      for error_segment in self.error_segments:
	 index_segment = 0
	 for segment in error_segment.segments:
	    if index_segment == error_segment.correct_index[index_segment]:
	       continue

	    index_segment_unit = 0
	    for segment_unit in segment:
	       margin = segment[0] - 

	       index_segment_unit += 1

	 index_segment += 1

	 index_error_segment += 1

      for error_segment in new_error_segments:
	 if len(error_segment.correct_segments) > 50:
	    print str(error_segment) + ' qtd ' + \
	       str(len(error_segment.correct_segments))
	    i = 0
	    e = []
	    for segment in error_segment.correct_segments:
	       w = error_segment.recognized_segments[i][0].score -\
		     segment[0].score
	       if w > 0:
		  w = -w
	       e.insert(0, w)
	       i += 1
#	    e.sort()
	    plt.figure()
	    plt.plot(e, label=str(error_segment))
	    plt.legend()
	    plt.savefig(str(i) + '.png')
      scores.sort()
      plt.plot(scores)
      plt.show()
