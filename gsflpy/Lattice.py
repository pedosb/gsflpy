from Sentence import Sentence
from Link import Link

class Lattice:
   def __init__(self, nodes, links, VERBOSE = None):
      if isinstance(nodes, list) and \
	    isinstance(links, list):
         self.nodes = nodes
         self.links = links
	 self.VERBOSE = VERBOSE
      #TODO: exception here
      else:
	 print 'nodes and links must be a list instance' + \
	       'was found:'
	 if isinstance(nodes, list):
	    print 'Links:' + str(links)
	 else:
	    print 'Nodes' + str(nodes)

   def __str__(self):
       nodes_str = ''
       for node in self.nodes:
          nodes_str += '\n' + str(node)

       links_str = ''
       for link in self.links.itervalues():
          links_str += '\n' + str(link)

       return nodes_str + '\n' + links_str

   def get_start_and_end_node(self):
       if self.VERBOSE:
	  print 'Search for start node and end node'
       #starts the nodes that is shown in links as 's' and as 'e'
       e_nodes = []
       s_nodes = []
       for link in self.links:
	  if link.e not in e_nodes:
	     e_nodes.append(link.e)
          if link.s not in s_nodes:
	     s_nodes.append(link.s)
       #check if some node is never shown as 'e' and as 's', to know
       #if there is a start node and an end node respectively
       end_nodes = []
       start_nodes = []
       for node in self.nodes:
	  if node not in e_nodes:
	     start_nodes.append(node)
	  if node not in s_nodes:
	     end_nodes.append(node)

       #TODO Think about an exception here
       if len(start_nodes) != 1:
	  print 'More than one start node in the lattice file'
	  print 'Nodes as start node found'
	  for node in start_nodes:
	     print str(node)
          exit(-1)
       if len(end_nodes) != 1:
	  print 'More than one end node in the lattice file'
	  print 'Nodes as end node found'
	  for node in end_nodes:
	     print str(node)
          exit(-1)
	  
       if self.VERBOSE:
	  print 'Start node and end node FOUND'

       return start_nodes[0], end_nodes[0]

   def prunning(self):
      if self.VERBOSE:
	 print 'Prunning of: ' + str(len(self.sentences)) + ' sentences'

      if self._MAX_SCORE_DIFF:
	 #Found bounds based on the max_frame_diff
	 self.sentences.sort(cmp=Sentence.cmp_frame, reverse=True)
	 max_frame_position = self.sentences[0]._frame_position - self._MAX_FRAME_DIFF
	 last_bound = 0
	 sub_sentences_bounds = []

	 for sentence in self.sentences:
	    if sentence._frame_position < max_frame_position:
	       actual_bound = self.sentences.index(sentence)+1
	       sub_sentences_bounds.append([last_bound, actual_bound])
	       last_bound = actual_bound
	       max_frame_position = sentence._frame_position - self._MAX_FRAME_DIFF

	 if last_bound != len(self.sentences):
	    sub_sentences_bounds.append([last_bound, len(self.sentences)])

	 print 'FOUND ' + str(len(sub_sentences_bounds)) + ' Bounds'
	 #Make prunning on the bounds based on max_score_diff
	 new_sentences = []
	 for bounds in sub_sentences_bounds:
#	    print 'Bound ' + str(sub_sentences_bounds.index(bounds)) + ':' + \
#		  str(self.sentences[bounds[0]]._score) + ' ' +\
#		  str(self.sentences[bounds[1]]._score)
	    sub_sentences = self.sentences[bounds[0]:bounds[1]]
	    sub_sentences.sort(cmp=Sentence.cmp_score, reverse=True)
#	    print 'len->sub_sentences ' + str(len(sub_sentences)) + ' ' +\
#		  str(self.sentences[bounds[0]]._score) + ' ' + str(self.sentences[bounds[1]]._score)
		  #+ ' ' + str(bounds[0]) + ' ' + str(bounds[1])
	    max_score = sub_sentences[0]._score - self._MAX_SCORE_DIFF
	    try:
	       if sub_sentences[0]._score < self.sentences_ready[0]._score:
		  continue
	    except IndexError:
	       pass
	    if sub_sentences[len(sub_sentences)-1]._score > max_score:
	       new_sentences += sub_sentences[:]
	       continue
	    for sentence in sub_sentences:
	       if sentence._score < max_score:
#		  print 'Passed until ' + str(sub_sentences.index(sentence))
		  new_sentences += sub_sentences[0:sub_sentences.index(sentence)]
		  break;
	 self.sentences = new_sentences

      elif self._MAX_WORDS:
	 new_sentences = []
	 for sentence in self.sentences:
	    if sentence._score < self.sentences_ready[0]._score:
	       continue
	    if len(sentence.nodes) <= self._MAX_WORDS:
	       new_sentences.append(sentence)

	 self.sentences = new_sentences

      else:
	 print 'WARNING: prunning not defined'
	 return
      if self.VERBOSE:
	 print 'The sentences was reduced to ' + str(len(self.sentences))

   def search_sentences_c(self, \
	 max_words = None):
      if max_words:
	 self._MAX_WORDS = int(max_words)
      else:
	 self._MAX_WORDS = None

      start_node, end_node = self.get_start_and_end_node()

      import gsflc

      links_c = []
      for link in self.links:
	 links_c.append([self.nodes.index(link.s), self.nodes.index(link.e)])

      sentences = gsflc.search(self.nodes.index(start_node),\
	    self.nodes.index(end_node),\
	    len(self.nodes),\
	    links_c,\
	    self._MAX_WORDS)

      self.sentences = []

      for sentence in sentences:
	 new_sentence = Sentence()
	 for link_index in sentence:
	    new_sentence.add(self.links[link_index])
	 self.sentences.insert(0, new_sentence)

      return self.sentences

   def search_sentences(self, \
	 max_words = None, \
	 max_score_diff = None, \
	 max_frame_diff = None):
      if max_words:
	 self._MAX_WORDS = int(max_words)
      else:
	 self._MAX_WORDS = None
      if max_score_diff and max_frame_diff:
	 self._MAX_SCORE_DIFF = max_score_diff
	 self._MAX_FRAME_DIFF = max_frame_diff
      else:
	 self._MAX_SCORE_DIFF = None
	 self._MAX_FRAME_DIFF = None

      start_node, end_node = self.get_start_and_end_node()
	 
      self.sentences = [Sentence()]
      self.sentences_ready = []
      to_remove = None
      sentence = self.sentences[0]
      count = 0
      sentence.add(start_node)
      self.links.sort(cmp=Link.cmp_s)
      nodes_s = []
      for link in self.links:
	 nodes_s.append(link.s)
      while True:
	 if count > 1000:
	    print sentence
	    count = 0
	 count += 1
#	 print sentence

	 if sentence.ready or len(sentence.nodes) >= self._MAX_WORDS:
	    to_remove = sentence
	    try:
	       sentence = self.sentences[self.sentences.index(sentence)+1]
	    except IndexError:
	       break
	    self.sentences.remove(to_remove)
	    continue

	 is_pri = True
	 last_node = sentence.last_node

	 index = nodes_s.index(last_node)
	 while True:
#	       print 'S=' + str(link.s.i) + ' E=' + str(link.e.i)
	    try:
	       if last_node == self.links[index].s:
		  if is_pri:
		     is_pri = False
		     sentence.add(self.links[index])
		  else:
		     new_sentence = sentence.copy()
		     new_sentence.add(self.links[index])
		     self.sentences.append(new_sentence)
		  index += 1
	       else:
		  break
	    except IndexError:
	       break

	 if sentence.last_node == end_node:
	    sentence.ready = True
	    self.sentences_ready.append(sentence)

      print len(self.sentences_ready)
      return self.sentences_ready

