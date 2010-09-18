from Link import Link
class Sentence():
   def __init__(self, link = None):
      self.links = []
      self.nodes = []
      self.last_node = None
      self._score = None
      self.ready = False
      if link:
	 self.add(link)

   def add(self, link):
      if isinstance(link, Link):
	 if not self._score:
	    self._score = 0
	 self.links.append(link)
	 if link.d:
	    for segment in link.d:
	       self._score += segment.score
	 if not self.last_node:
	    self.nodes.append(link.s)
	 self.nodes.append(link.e)
	 self.last_node = link.e
      else:
	 #TODO: Create an exception
	 pass

   def __str__(self):
      string = ''
      for node in self.nodes:
	 string += ' ' + node.w
      return string.strip()

   def __cmp__(self, other):
      """
      Compare based on the score of the entire sentence.
      """
      if self._score > other._score:
	 return -1
      elif self._score < other._score:
	 return 1
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





