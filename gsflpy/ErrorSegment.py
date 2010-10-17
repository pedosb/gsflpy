class ErrorSegment(object):
   def __init__(self, \
	 segments, \
	 correct_index, \
	 start_time, \
	 file_name):
      """
      Create an ErrorSegment for one specific type of error, it is,
      we do not care about the time it spend in each state but
      the sequence of states, of both, correct and recognized sentence.
      The segments list must be sorted that is the correct sentence must
      be the first one, and correct_index the index in this list
      that corresponds to the correct sentence.
      """
      self.segments = []
      self.correct_index = []
      self.start_time = []
      self.file_name = []

      self.add(segments, 
	       correct_index, 
	       start_time, 
	       file_name)

      self.recognized_states = self.set_state_string(
	    self.segments[0][0])
      self.correct_states = self.set_state_string(
	    self.segments[0][self.correct_index[0]])

   def set_state_string(self, segments):
      last_state = None
      state_string = ""
      for segment in segments:
	 if not last_state or \
	       segment.state != last_state:
	    last_state = segment.state
	    state_string += str(segment.state)
      return state_string

   def add(self, 
	 segments, 
	 correct_index, 
	 start_time, 
	 file_name):
      if (segments and 
	    correct_index != None and 
	    start_time != None and 
	    (file_name or file_name == "")):
	 self.segments.append(segments)
	 self.correct_index.append(correct_index)
	 self.start_time.append(start_time)
	 self.file_name.append(file_name)
      else:
	 #TODO exception here
	 print 'WARNING: Error segment with a broken argument'
	 exit(-1)

   def clean(self):

      import logging
      logging.basicConfig(filename='log/clean.log',
	    filemode='w',
	    level=logging.INFO)

      segments = []
      correct_index = []
      start_time = []
      file_name = []

      logging.info('Starting clean for ' +
	    str(self) + ' with ' + str(len(self.file_name)) +
	    ' samples.')

      index = 0
      while len(self.file_name) != 0:
	 index_file_name = -1
	 while True:
	    try:
	       index_file_name = file_name.index(
		     self.file_name[index],
		     index_file_name + 1,
		     len(file_name))
	       #Test if there already a copy of the same
	       #start time and the length of the region.
	       if self.start_time[index] == start_time[
		     index_file_name]:
		  if len(self.segments[index][0]) == len(
			segments[index_file_name][0]):
		     del self.segments[index]
		     del self.correct_index[index]
		     del self.start_time[index]
		     del self.file_name[index]
		     break
	    except ValueError:
	       segments.insert(0, self.segments.pop(index))
	       correct_index.insert(0, self.correct_index.pop(index))
	       start_time.insert(0, self.start_time.pop(index))
	       file_name.insert(0, self.file_name.pop(index))
	       break

      self.segments = segments
      self.correct_index = correct_index
      self.start_time = start_time
      self.file_name = file_name

      logging.info('Stopped clean with '
	    + str(len(self.file_name)) + ' samples.')

   def __cmp__(self, other):
      if self.correct_states == other.correct_states and \
	    self.recognized_states == other.recognized_states:
	 return 0
      else:
	 return -1

   def __str__(self):
      return 'Recognized: ' + self.recognized_states + \
	    ' Correct: ' + self.correct_states

