class ErrorSegment():
   def __init__(self, \
	 correct_segments, \
	 recognized_segments, \
	 start_time, \
	 file_name):
      if correct_segments and \
	    recognized_segments and \
	    start_time != None and \
	    (file_name or file_name == ""):
	 self.correct_segments = []
	 self.recognized_segments = []
	 self.start_time = []
	 self.file_name = []

	 self.add(correct_segments, \
		  recognized_segments, \
		  start_time, \
		  file_name)

	 self.correct_states = self.set_state_string(\
	       self.correct_segments[0])
	 self.recognized_states = self.set_state_string(\
	       self.recognized_segments[0])
      else:
	 print 'WARNING: Error segment with broken argument'

   def set_state_string(self, segments):
      last_state = None
      state_string = ""
      for segment in segments:
	 if not last_state or \
	       segment.state != last_state:
	    last_state = segment.state
	    state_string += str(segment.state)
      return state_string

   def add(self, \
	 correct_segments, \
	 recognized_segments, \
	 start_time, \
	 file_name):
      if correct_segments and \
	    recognized_segments and \
	    start_time != None and \
	    (file_name or file_name == ""):
	 self.correct_segments.append(correct_segments)
	 self.recognized_segments.append(recognized_segments)
	 self.start_time.append(start_time)
	 self.file_name.append(file_name)

   def cmp_phoneme(self, other):
      if self.correct_states == other.correct_states and \
	    self.recognized_states == other.recognized_states:
	 return 0
      else:
	 return -1

   def __str__(self):
      return 'Recognized: ' + self.recognized_states + \
	    ' Correct: ' + self.correct_states

