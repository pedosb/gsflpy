class Arff():
   def __init__(self):
      self.matrix = dict()
      self.EMPTY_SCORE = 1

   def add(self, line):
      if not isinstance(line, dict):
	 #TODO exception here
	 print 'ERROR: line to add must be a' + \
	       'dictionary with score values for each hmm state'
      if len(line) == 0:
	 return

      if len(self.matrix) > 0:
	 matrix_row_count = len(self.matrix[self.matrix.keys()[0]])
      else:
	 matrix_row_count = 0

      for line_key in line:
	 if not self.matrix.has_key(line_key):
	    self.matrix[line_key] = matrix_row_count * [self.EMPTY_SCORE]
	 self.matrix[line_key].append(line[line_key])

      for matrix_key in self.matrix:
	 if len(self.matrix[matrix_key]) == matrix_row_count:
	    self.matrix[matrix_key].append(self.EMPTY_SCORE)

   def __str__(self):
      if len(self.matrix) <= 0:
	 return ""
      SPACE = 2
      PRECISION = 5
      WIDTH = 11
      format_key = ('{0: ^' + str(WIDTH) + '}' + \
	    (SPACE * ' ')).format
      format_score = ('{0:0<' + str(WIDTH) + \
	    '.' + str(PRECISION) + 'f}' + (SPACE * ' ')).format

      str_matrix = ""
      for key in self.matrix.keys():
	 str_matrix += format_key(str(key))
      str_matrix += '\n'

      for i in range(len(self.matrix[self.matrix.keys()[0]])):
	 for key in self.matrix.keys():
	    str_matrix += format_score((self.matrix[key][i]))
	 str_matrix += '\n'

      return str_matrix
