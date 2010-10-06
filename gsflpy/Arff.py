#!/usr/bin/env python

class Arff():
   def __init__(self):
      self.matrix = dict()
      self.matrix_row_count = 0
      self.EMPTY_SCORE = 1

   def add(self, line):
      """
      Add a new sample in the current arff file.
      The line must be one dictionary with a single sample of the attribute.

      If the attribute is not known by the arff it is added with all unknown
      values setted to EMPTY_SCORE
      """
      if line == None:
	 return
      if not isinstance(line, dict):
	 #TODO exception here
	 print 'ERROR: line to add must be a' + \
	       'dictionary with score values for each hmm state'
	 return
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

      self.matrix_row_count += 1

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

   def write(self, file_name):
      if len(self.matrix) <= 0:
	 return ""

      f = open(file_name, 'w')

      f.write("@RELATION 'lattices - 15best'\n")
      for key in self.matrix.keys():
	 f.write('@ATTRIBUTE ' + str(key) + ' NUMERIC\n')

      f.write('@DATA\n')

      f.flush()
      f.close()
      self.append(file_name)

   def append(self, file_name):
      """
      Append data to a specific arff file.
      Not that it does not check if the attribute sequence and length
      is compatible it just append data to it.
      """
      f = open(file_name, 'a')

      str_data = ""
      for i in range(len(self.matrix[self.matrix.keys()[0]])):
	 for key in self.matrix.keys():
	    str_data += str(self.matrix[key][i]) + ','
	 f.write(str_data[:len(str_data)-1] + '\n')
	 str_data = ""

      f.flush()
      f.close()

   def clean(self):
      for key in self.matrix:
	 self.matrix[key] = []
      self.matrix_row_count = 0

def get_attributies(file_name):
   """
   Return a list of attributies in this arff file
   and the file descriptor opened (the lasted read line
   was that with the @data
   """
   attributies = []
   f = open(file_name)
   line = f.readline()
   while (line != ''):
      if line != '\n':
	 line_splitted = line.split()
	 argument = line_splitted[0].lower()
	 if argument == '@attribute':
	    attributies.append(line_splitted[1])
	 elif argument == '@data':
	    break
      line = f.readline()

   return attributies, f

def get_sample(arff_file, attributies_list):
   line = arff_file.readline()
   if line == '':
      return None
   elif line == '\n':
      return dict()
   attributies = dict()
   index_attribute = 0
#   print 'line ', len(line.split(',')), 'att ', len(attributies_list)
   for attribute in line.split(','):
      attributies[str(attributies_list[index_attribute])] =\
	    attribute.strip()
      index_attribute += 1

   if len(attributies_list) != index_attribute:
      print 'Warning: Attribute length is different of the sample.'

   return attributies


def usage():
   print 'Usage:'
   print ('   ', sys.argv[0],
	 '-a <arff_list_file> -o <out_file> (-c)')
   print '    -a File with a list of arff file to manipulate (one per line)'
   print '    -o Arff file out resulted of the manipulation'
   print '    -c Contatenate all the input files in one'
   exit(-1)

import sys
if __name__=="__main__":
   if len(sys.argv) == 1:
      usage()

   arff = Arff()
   INPUT_FILE_LIST = None
   OUT_ARFF_FILE = None
   CONCATENATE = None

   index = 1
   while index < len(sys.argv):
      input = sys.argv[index]
      if input[0] == '-':
	 option = input[1:len(input)]
	 if option == 'a':
	    INPUT_FILE_LIST = []
	    index += 1
	    for line in open(sys.argv[index]):
	       INPUT_FILE_LIST.append(line.strip())
	 if option == 'o':
	    index += 1
	    OUT_ARFF_FILE = sys.argv[index]
	 if option == 'c':
	    CONCATENATE = True
      else:
	 usage()
      index += 1

   all_attributies = []
   attributies = []
   files = []
   for in_file_name in INPUT_FILE_LIST:
      actual_attrributies, actual_file = get_attributies(in_file_name)
      files.append(actual_file)
      attributies.append(actual_attrributies)
      all_attributies += actual_attrributies

   for attribute in all_attributies:
      arff.matrix[str(attribute)] = []
   arff.write(OUT_ARFF_FILE)

   index_file = 0
   for file in files:
      sample = ''
      while sample != None:
	 sample = get_sample(file, attributies[index_file])
	 arff.add(sample)
	 if arff.matrix_row_count % 500 == 0:
	    print index_file
	    arff.append(OUT_ARFF_FILE)
	    arff.clean()

      index_file += 1

   arff.append(OUT_ARFF_FILE)
