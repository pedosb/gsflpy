from Link import Link
from Node import Node
from Lattice import Lattice
from ReadLattice import ReadLattice

def find_correct(sentences, correct_sentence):
   if correct_sentence == None or correct_sentence == '':
      return sentences[0], None
   count = 0
   for sentence in sentences:
      if str(sentence) == correct_sentence:
	 return sentence, count
      count += 1

   return None, None

def get_sentences(lattice_ops):
   """
   lattice_ops must be a tuple with:
      (lat_file_name, max_nodes, correct_sentence)
   """
   read = ReadLattice()
   lattice = read.parse(lattice_ops[0])
   sentences = lattice.search_sentences_c(lattice_ops[1])
   correct_sentence = None
   correct_sentence_index = None

   if len(sentences) < 1:
      print 'WARNING: No sentences found.'
      return None, None, lattice

   print 'Recognized:'
   print sentences[0],sentences[0]._score
   if lattice_ops[2] == '' or lattice_ops[2] == None:
      return sentences, None, lattice

   correct_sentence, correct_sentence_index = \
	 find_correct(sentences, lattice_ops[2])

   if not correct_sentence:
      print 'WARNING: Correct sentence not found.'
      return sentences, None, lattice
   print 'Correct was the sentence number',correct_sentence_index
   print sentences[correct_sentence_index],sentences[correct_sentence_index]._score

   return sentences, correct_sentence_index, lattice

class Sentence(object):
   def __init__(self, link = None):
      self.links = []
      self.nodes = []
      self.last_node = None
      self.ready = False
      self._score = 0
      self._frame_position = 0
      if link:
	 self.add(link)

   def add(self, link):
      if isinstance(link, Link):
	 self.links.append(link)
	 if link.d:
	    for segment in link.d:
	       self._score += segment.score
	       self._frame_position += segment.length
	 if not self.last_node:
	    self.nodes.append(link.s)
	 self.nodes.append(link.e)
	 self.last_node = link.e
      elif isinstance(link, Node):
	 self.nodes.append(link)
	 self.last_node = link
      else:
	 #TODO: Create an exception
	 print 'WARNING: Trying to add something into a sentence that is not a link'
	 pass

   def __str__(self):
      string = ''
      for node in self.nodes:
	 string += ' ' + node.w
      return string.strip()

   def cmp_score(self, other):
      """
      Compare based on the score of the entire sentence.
      """
      if self._score > other._score:
	 return 1
      elif self._score < other._score:
	 return -1
      else:
	 return 0

   def cmp_frame(self, other):
      """
      Compare based on the frame_position.
      """
      if self._frame_position > other._frame_position:
	 return 1
      if self._frame_position < other._frame_position:
	 return -1
      else:
	 return 0

   def copy(self):
      """
      Create a copy of the sentence.
      Warnning: It does not copy the last node
      """
      sentence = Sentence()
      for link in self.links[0:len(self.links)-1]:
	 sentence.add(link)
      return sentence

   def norm_segments(self):
      """
      Check if any of the segments in the sentence has
      more than one frame per state, if it has, we
      copy it to have only one state per frame.
      """
      self.segments = []
      for link in self.links:
	 if link.d:
	    for segment in link.d:
	       for i in range(int(segment.length*100)):
		  self.segments.append(segment)

   def recalc_score(self):
      """
      This will recalculate the score based on segments so it must be available and norm.
      """
      if not self.segments:
	 return 

      old_score = self._score
      self._score = 0
      for segment in self.segments:
	 self._score += segment.score
      if old_score != self._score:
	 print 'gain in sentence'
	 print self
