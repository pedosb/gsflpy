class Lattice:
   def __init__(self, nodes, links):
      self.nodes = nodes
      self.links = links

   def __str__(self):
       nodes_str = ''
       for node in self.nodes.itervalues():
          nodes_str += '\n' + str(node)

       links_str = ''
       for link in self.links.itervalues():
          links_str += '\n' + str(link)

       return nodes_str + '\n' + links_str

    def search_sentences(self):
       e_nodes = s_nodes = []
       for link in self.links:
	  e_nodes.append(link.e)
	  s_nodes.append(link.s)
       end_nodes = start_nodes = []
       for node in nodes:
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
       if len(end_nodes) != 1:
	  print 'More than one end node in the lattice file'
	  print 'Nodes as end node found'
	  for node in end_nodes:
	     print str(node)

       start_node = start_nodes[0]
       del start_nodes
       end_node = end_nodes[0]
       del end_nodes

       sentences = []
       for link in self.links:
	  if start_node == link.s:
	     sentences.append(Sentence(link)
       sentences.append(Sentence())
       while True:
	  for link in self.links:

