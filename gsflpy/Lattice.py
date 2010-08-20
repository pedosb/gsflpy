from Sentence import Sentence
from Link import Link

class Lattice:
   def __init__(self, nodes, links):
      if isinstance(nodes, dict) and \
	    isinstance(links, dict):
         self.nodes = nodes
         self.links = links
      #TODO: exception here
      else:
	 print 'nodes and links must be a dict instance' + \
	       'was found:'
	 if isinstance(nodes, dict):
	    print 'Links:' + str(links)
	 else:
	    print 'Nodes' + str(nodes)

   def __str__(self):
       nodes_str = ''
       for node in self.nodes.itervalues():
          nodes_str += '\n' + str(node)

       links_str = ''
       for link in self.links.itervalues():
          links_str += '\n' + str(link)

       return nodes_str + '\n' + links_str

   def search_sentences(self):
       #starts the nodes that is shown in links as 's' and as 'e'
       e_nodes = []
       s_nodes = []
       for link in self.links.itervalues():
	  if link.e not in e_nodes:
	     e_nodes.append(link.e)
          if link.s not in s_nodes:
	     s_nodes.append(link.s)
       #check if some node is never shown as 'e' and as 's', to know
       #if there is a start node and an end node respectively
       end_nodes = []
       start_nodes = []
       for node in self.nodes.itervalues():
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

       #Mark the start and end nodes
       start_node = start_nodes[0]
       del start_nodes
       end_node = end_nodes[0]
       del end_nodes

       #Start sentences by the start node
       sentences = []
       for link in self.links.itervalues():
	  if start_node == link.s:
	     sentences.append(Sentence(link))

       #Search sentences
       sentence = sentences[0]
       while True:
	  acessed_sentence = False
	  for link in self.links.itervalues():
	     #if there is a link that start with the last node of the sentence
	     if sentence.last_node == link.s:
		#if the sentence has already make a trasition with the
		#last_node we need to make a copy of the sentence to do
		# a new transition
		if acessed_sentence:
		   new_sentence = sentence.copy()
		   new_sentence += link
		   sentences.append(new_sentence)
	        else:
		   sentence += link
		   acessed_sentence = True
	  if sentence.last_node == end_node:
	     sentence.ready = True
	  for sentence in sentences:
             if not sentence.ready:
                break
	  if sentence.ready:
	     break
       return sentences
	  






















