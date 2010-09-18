import matplotlib.pyplot as plt
from ErrorSegment import ErrorSegment
import util
#TODO This is not a good name
class ErrorSegments():
   def __init__(self,error_segments):
      self.error_segments = error_segments

   def most_different(self):
      new_error_segments = []
      scores = []
      for error_segment in self.error_segments:
	 index_correct_segment = 0
	 for correct_segment in error_segment.correct_segments:
	    index_segment = 0
	    #TODO find the smallest float and put it here
	    small = None
	    for segment in correct_segment:
	       e = error_segment.recognized_segments\
		     [index_correct_segment][index_segment].score\
		     - segment.score
	       if small == None:
		  small = [index_segment, e]
	       if e < small[1]:
		  small = [index_segment, e]
	       index_segment += 1

	    scores.insert(0, small[1])
	    util.add_error_segment(new_error_segments,\
		  ErrorSegment([error_segment.correct_segments\
			[index_correct_segment][small[0]]],\
		     [error_segment.recognized_segments\
			[index_correct_segment][small[0]]],\
		     int(error_segment.start_time[index_correct_segment]) + small[0],\
		     error_segment.file_name[index_correct_segment]))
	    index_correct_segment += 1

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
