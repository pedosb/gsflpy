from Link import Link
from Node import Node
class Sentence():
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
