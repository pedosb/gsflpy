def ErrorSegment():
   def __init__(self, \
	 correct_segments = None, \
	 recognized_segments = None, \
	 start_time = None, \
	 file_name = None):
      self.correct_segments = []
      self.recognized_segments = []
      self.start_time = []
      self.file_name = []
      if correct_segments and \
	    recognized_segments and \
	    start_time and \
	    file_name:
	 self.add(correct_segments, \
	       recognized_segments, \
	       start_time, \
	       file_name)

   def cmp_phoneme(self, other):
      if self.correct_phoneme == other.correct_phoneme && \
	    self.recognized_phoneme == other.recognized_phoneme:
	 return 0
      else:
	 return -1
