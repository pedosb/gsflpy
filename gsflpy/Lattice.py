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
