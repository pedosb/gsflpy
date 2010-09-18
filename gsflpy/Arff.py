class Arff():
   def __init__(self):
      matrix = dict()
      EMPTY_SCORE = 1

   def add(self, line):
      if not isinstance(line, dict):
	 #TODO exception here
	 print 'ERROR: line to add must be a' + \
	       'dictionary with score values for each hmm state'
      if len(line) == 0:
	 return

      if len(self.matrix.keys()) > 0:
	 matrix_row_count = len(self.matrix[self.matrix.keys()[0]])
      else:
	 matrix_row_count = 0

      for line_key in line:
	 if not self.matrix.has_hey(line_key):
	    self.matrix[line_key] = matrix_row_count * [EMPTY_SCORE]
	 self.matrix[line_key].append(line[line_key])

      for matrix_key in self.matrix:
	 if len(self.matrix[matrix_key]) == matrix_row_count:
	    self.matrix[matrix_key].append(EMPTY_SCORE)
   def __str__(self):
      str_matrix = dict()
      for matrix_key in self.matrix:
	 str_matrix[matrix_key] = ""
	 for score in self.matrix[matrix_key]:
	    str_matrix[matrix_key] += str(score) + ' '
      for str_matrix_
