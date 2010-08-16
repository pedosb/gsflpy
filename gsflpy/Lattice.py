class Lattice:
    def __init__(self, nodes, links):
	self.nodes = nodes
	self.links = links
    def __str__(self):
	nodes_str = ''
        for node in self.nodes.itervalues():
	    nodes_str = nodes_str + '\n' + str(node)
	return nodes_str
