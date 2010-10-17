class Segment(object):
   def __init__(self, \
	 state, \
	 length, \
	 score):
      self.state = state
      self.length = float(length)
      self.score = float(score)

   def __str__(self):
      string = ''
      string += self.state + "," + \
	    str(self.length) + ',' + \
	    str(self.score) + ':'
      return string
